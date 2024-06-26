from django import forms
from todo.models import Todo


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = (
            'description',
            'category',
            'status',
            'priority',
            'due_date',
            'notes',
        )


class SearchForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = (
            'description',
            'category',
            'status',
            'priority',
            'due_date',
        )
