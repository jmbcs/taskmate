from http.client import HTTPResponse
from sre_constants import SUCCESS

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from todo.forms import TodoForm  # Create your views here.
from todo.models import Todo


@login_required
@require_http_methods(["GET"])
def todo_list(request: HttpRequest):
    todos = Todo.objects.filter(assigned_user=request.user)
    context = {"todos": todos}
    return render(request, 'todo/todo_list.html', context)


@login_required
@require_http_methods(["DELETE"])
def todo_delete(request: HttpRequest, pk: int):
    try:
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return HttpResponse({"success": True})
    except Todo.DoesNotExist:
        return HttpResponse({"error": "Todo item does not exist"}, status=404)
    except Exception as e:
        return HttpResponse({"error": str(e)}, status=500)


@login_required
# @require_http_methods(["GET"])
def todo_create(request: HttpRequest):
    context = {
        'Todo': Todo,
    }
    return render(request, 'todo/snippet/todo_create.html', context)


@login_required
def todo_submit(request: HttpRequest):

    form = TodoForm(request.POST)

    if form.is_valid():
        todo = form.save(commit=False)
        todo.assigned_user = request.user
        todo.save()

        context = {'todo': todo}
        return render(request, 'todo/todo_list.html#todo-item-row', context)
    return render(request, 'todo/todo_list.html')


@login_required
def todo_update(request: HttpRequest, pk: int):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.updated_at = timezone.now()
            todo.assigned_user = request.user
            todo.save()
            print(todo)

            # Return the updated todo item as a partial HTML
            context = {'todo': todo}

            return render(
                request, 'todo/partial/todo_partial_row.html#todo-item', context
            )
    else:
        # Pre-fill the form with the existing todo item's data
        form = TodoForm(instance=todo)

    return render(
        request, 'todo/partial/todo_partial_edit.html', {'form': form, 'todo': todo}
    )


@login_required
def todo_update_details(request: HttpRequest, pk: int):
    todo = get_object_or_404(Todo, pk=pk)
    context = {'todo': todo}
    print(todo)
    return render(
        request, 'todo/partial/todo_partial_detail.html#todo-more-details', context
    )


@login_required
def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    form = TodoForm(instance=todo)
    print(todo)
    context = {'form': form, 'todo': todo, 'Todo': Todo}

    return render(request, 'todo/partial/todo_partial_edit.html#todo-edit', context)


# update todo_details_{{ todo.id }
