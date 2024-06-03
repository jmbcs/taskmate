from django.contrib import admin
from todo.models import Todo

# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    list_display = ['assigned_user', 'description', 'status', 'created_at']


admin.site.register(Todo, TodoAdmin)
