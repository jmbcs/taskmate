from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from todo.models import Todo

# Create your views here.


@login_required
def todo_list(request: HttpRequest):
    todos = Todo.objects.filter(assigned_user=request.user)

    context = {"todos": todos}
    return render(request, 'todo/todo_list.html', context)


@login_required
def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    print(todo)
    return render(request, 'todo/partial/todo_detail.html', {'todo': todo})
