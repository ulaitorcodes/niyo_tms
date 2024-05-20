
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, ProjectSerializer, SprintSerializer, AddMembersSerializer
from niyo_tms.app.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from niyo_tms.app.models import Project, Sprint
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        project.members.add(self.request.user)
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.filter(members=user)
        print(f"User: {user}, Projects: {projects}")
        return projects


    def get_object(self):
        obj = super().get_object()
        if self.request.user not in obj.members.all():
            raise PermissionDenied("You do not have permission to access this project.")
        return obj
    

    @action(detail=True, methods=['post'], url_path='add-members', permission_classes=[IsAuthenticated])
    def add_members(self, request, pk=None):
        project = self.get_object()
        serializer = AddMembersSerializer(data=request.data)
        if serializer.is_valid():
            user_ids = serializer.validated_data['user_ids']
            existing_member_ids = project.members.values_list('id', flat=True)
            already_members = [user_id for user_id in user_ids if user_id in existing_member_ids]
            if already_members:
                raise ValidationError(f"Users with IDs {already_members} are already members of this project.")
            users = User.objects.filter(id__in=user_ids)
            project.members.add(*users)
            return Response({'status': 'members added'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class SprintViewSet(viewsets.ModelViewSet):
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Filter sprints based on project membership
        return Sprint.objects.filter(project__members=user) | Sprint.objects.filter(project__created_by=user)

    def create(self, request, *args, **kwargs):
        # Extract project ID from request data
        project_id = request.data.get('project')
        
        # Check if project exists and if the current user created it
        try:
            project = Project.objects.get(id=project_id, created_by=request.user)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found or you are not the creator'}, status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)
    

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(sprint__project__members=user)
    

class MoveTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the user is the owner or the task is assigned to the user
        if task.created_by != request.user and task.assigned_to != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        if new_status not in ['todo', 'in_progress', 'done']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        task.status = new_status
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AssignTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the request user is the creator of the task or the creator of the project
        if task.created_by != request.user and (task.sprint is None or task.sprint.project.created_by != request.user):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get the user to assign the task to
        assigned_to_id = request.data.get('assigned_to')
        try:
            assigned_to = User.objects.get(pk=assigned_to_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the user is a member of the project
        if task.sprint:
            project = task.sprint.project
            if assigned_to not in project.members.all():
                return Response({'error': 'User is not a member of the project'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Assign the task
        task.assigned_to = assigned_to
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)