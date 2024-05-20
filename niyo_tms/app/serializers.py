from rest_framework import serializers
from .models import Task
from niyo_tms.users.api.serializers import UserSerializer
from niyo_tms.app.models import Project, Sprint
from django.contrib.auth import get_user_model

User = get_user_model()




class AddMembersSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    def validate_user_ids(self, value):
        users = User.objects.filter(id__in=value)
        if len(users) != len(value):
            raise serializers.ValidationError("One or more user IDs are invalid.")
        return value


# class TaskSerializer(serializers.ModelSerializer):
#     created_by = UserSerializer(read_only=True)
#     assigned_to = UserSerializer(read_only=True)

#     class Meta:
#         model = Task
#         fields = ['id', 'title', 'description', 'project', 'sprint', 'assigned_to', 'status', 'due_date', 'created_by', 'created_at', 'updated_at']
#         read_only_fields = ['created_at', 'updated_at']

#     def create(self, validated_data):
#         project_data = validated_data.pop('project', None)
#         sprint_data = validated_data.pop('sprint', None)
#         assigned_to_data = validated_data.pop('assigned_to', None)

#         if project_data:
#             project = project_data
#             validated_data['project'] = project

#         if sprint_data:
#             sprint = sprint_data
#             validated_data['sprint'] = sprint

#         if assigned_to_data:
#             assigned_to = assigned_to_data
#             validated_data['assigned_to'] = assigned_to

#         task = Task.objects.create(**validated_data)
#         return task

    def update(self, instance, validated_data):
        project_data = validated_data.pop('project', None)
        sprint_data = validated_data.pop('sprint', None)
        assigned_to_data = validated_data.pop('assigned_to', None)

        if project_data:
            project = project_data
            instance.project = project

        if sprint_data:
            sprint = sprint_data
            instance.sprint = sprint

        if assigned_to_data:
            assigned_to = assigned_to_data
            instance.assigned_to = assigned_to

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.save()
        return instance
    

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ['id', 'name', 'project', 'start_date', 'end_date', 'active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'project': {'required': True}
        }


class ProjectSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    sprints = SprintSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'sprint', 'assigned_to', 'status', 'due_date', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'sprint': {'required': True}
        }

    def validate_sprint(self, value):
        if value is None:
            raise serializers.ValidationError("Sprint is required.")
        
        user = self.context['request'].user
        if not Sprint.objects.filter(id=value.id, project__created_by=user).exists():
            raise serializers.ValidationError("Sprint must be created by the user.")
        return value

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().update(instance, validated_data)