from django.contrib import admin
from niyo_tms.app.models import (
    Project, Task, Sprint
)

# Register your models here.
admin.register(Project)
admin.register(Sprint)
admin.register(Task)

