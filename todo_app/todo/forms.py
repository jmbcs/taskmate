from django import forms
from todo.models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('task_description', 'task_status')
