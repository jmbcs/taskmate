from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from todo.forms import SearchForm, TodoForm  # Create your views here.
from todo.models import Todo


@csrf_protect
@login_required
@require_http_methods(["GET"])
def todo_list(request: HttpRequest):
    todos = Todo.objects.filter(assigned_user=request.user).order_by('due_date')
    context = {"todos": todos, "Todo": Todo}
    return render(request, 'todo/todo_list.html', context)


@csrf_protect
@login_required
@require_http_methods(["GET"])
def todo_search(request: HttpRequest):
    todos = Todo.objects.filter(assigned_user=request.user)
    todos = Todo.objects.filter(assigned_user=request.user).order_by('due_date')

    description = request.GET.get('description')
    category = request.GET.get('category')
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    due_date = request.GET.get('due_date')

    if description:
        todos = todos.filter(description__icontains=description)
    if category:
        todos = todos.filter(category=category)
    if status:
        todos = todos.filter(status=status)
    if priority:
        todos = todos.filter(priority=priority)
    if due_date:

        start_date_str, end_date_str = due_date.split(' to ')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        todos = todos.filter(due_date__range=(start_date, end_date))

    context = {"todos": todos, "Todo": Todo}
    return render(request, 'todo/todo_table.html#todo-rows', context)


@csrf_protect
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


@csrf_protect
@login_required
@require_http_methods(["POST"])
def todo_submit(request: HttpRequest):

    form = TodoForm(request.POST)

    if form.is_valid():
        todo = form.save(commit=False)
        todo.assigned_user = request.user
        todo.save()
        context = {'todo': todo}

    todos = Todo.objects.filter(assigned_user=request.user).order_by('due_date')
    context = {
        'Todo': Todo,
        'todos': todos,
    }
    return render(request, 'todo/todo_table.html#todo-rows', context)


@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def todo_update(request: HttpRequest, pk: int):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.updated_at = timezone.now()
            todo.assigned_user = request.user
            todo.save()

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


@csrf_protect
@login_required
@require_http_methods(["GET"])
def todo_update_details(request: HttpRequest, pk: int):
    todo = get_object_or_404(Todo, pk=pk)
    context = {'todo': todo}

    return render(
        request, 'todo/partial/todo_partial_detail.html#todo-more-details', context
    )


@csrf_protect
@require_http_methods(["GET"])
@login_required
def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    form = TodoForm(instance=todo)
    context = {'form': form, 'todo': todo, 'Todo': Todo}
    return render(request, 'todo/partial/todo_partial_edit.html#todo-edit', context)
