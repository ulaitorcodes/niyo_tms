from django.urls import path
from .views import TaskViewSet, ProjectViewSet

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from niyo_tms.app.views import ProjectViewSet, MoveTaskView, SprintViewSet, AssignTaskView

project_list = ProjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

project_detail = ProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


add_members = ProjectViewSet.as_view({
    'post': 'add_members'
})


sprint_list = SprintViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

sprint_detail = SprintViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


task_list = TaskViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

task_detail = TaskViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('projects/', project_list, name='project-list'),
    path('projects/<int:pk>/', project_detail, name='project-detail'),
    path('projects/<int:pk>/add-members/', add_members, name='project-add-members'),
    path('sprints/', sprint_list, name='sprint-list'),
    path('sprints/<int:pk>/', sprint_detail, name='sprint-detail'),
    path('tasks/', task_list, name='task-list'),
    path('tasks/<int:pk>/', task_detail, name='task-detail'),
    path('tasks/<int:pk>/move/', MoveTaskView.as_view()),
    path('tasks/<int:pk>/assign/', AssignTaskView.as_view(), name='assign-task'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
