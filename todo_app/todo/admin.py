from django.contrib import admin
from todo.models import Todo

# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    list_display = ['assigned_user', 'task_description', 'task_status', 'created_at']


admin.site.register(Todo, TodoAdmin)
