from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
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
def delete_todo(request, pk: int):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('todo_list')


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
        todo.assigned_user = request.user
        todo.save()

        # return a todoitem-partial html

        context = {'todo': todo}
        return render(request, 'todo/todo_list.html#todo-item', context)
    return render(request, 'todo/todo_list.html')


@login_required
def update_todo(request: HttpRequest, pk):
    todo = get_object_or_404(Todo, pk=pk)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)

            todo.updated_at = timezone.now()
            print(todo.updated_at)
            todo.assigned_user = request.user
            todo.save()

            # Return the updated todo item as a partial HTML
            context = {'todo': todo}
            return render(request, 'todo/todo_list.html#todo-item', context)
    else:
        # Pre-fill the form with the existing todo item's data
        form = TodoForm(instance=todo)

    return render(request, 'todo/partial/edit_todo.html', {'form': form, 'todo': todo})


@login_required
def edit_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    form = TodoForm(instance=todo)
    return render(
        request,
        'todo/partial/edit_todo.html',
        {'form': form, 'todo': todo, 'Todo': Todo},
    )
