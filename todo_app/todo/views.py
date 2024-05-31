from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from todo.forms import TodoForm  # Create your views here.
from todo.models import Todo


@login_required
def todo_list(request: HttpRequest):
    todos = Todo.objects.filter(assigned_user=request.user)

    context = {"todos": todos}
    return render(request, 'todo/todo_list.html', context)


@login_required
def todo_detail(request, pk: int):
    todo = get_object_or_404(Todo, pk=pk)
    return render(request, 'todo/partial/todo_detail.html', {'todo': todo})


@login_required
def todo_create(request: HttpRequest):
    context = {
        'Todo': Todo,
    }
    return render(request, 'todo/partial/todo_create.html', context)


@login_required
def submit_todo(request: HttpRequest):
    form = TodoForm(request.POST)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()

        # return a todoitem-partial html

        context = {'todo': todo}
        return render(request, 'index.html#todoitem-partial', context)
