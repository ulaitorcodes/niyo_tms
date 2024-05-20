from django.db import models
from django.contrib.auth import get_user_model

from django.utils import timezone

User = get_user_model()

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name='projects')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Sprint(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sprints')
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.active:
            Sprint.objects.filter(project=self.project, active=True).exclude(pk=self.pk).update(active=False)
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.active and self.start_date <= timezone.now().date() <= self.end_date


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, related_name='tasks', null=True, blank=True)  # Add the sprint field
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')
    ], default='todo')
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title