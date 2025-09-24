from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Task

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']
    list_filter = ['role']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'assigned_to', 'status', 'worked_hours']
    fields = ['title', 'description', 'assigned_to', 'status', 'due_date', 'completion_report', 'worked_hours']

    def save_model(self, request, obj, form, change):
        if obj.status == 'completed':
            if not obj.completion_report or obj.worked_hours is None:
                from django.core.exceptions import ValidationError
                raise ValidationError("Completion report and worked hours are required when marking task as completed.")
        super().save_model(request, obj, form, change)

admin.site.register(Task, TaskAdmin)
