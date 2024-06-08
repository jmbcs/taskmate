import todo.views as todo_views
from django.urls import path

# Create your views here.
urlpatterns = [
    path('', todo_views.todo_list, name='todo_list'),
    path('submit/', todo_views.todo_submit, name='todo_submit'),
    path('search/', todo_views.todo_search, name='todo_search'),
    path('<int:pk>/edit/', todo_views.todo_edit, name='todo_edit'),
    path('<int:pk>/update/', todo_views.todo_update, name='todo_update'),
    path(
        '<int:pk>/update_details/',
        todo_views.todo_update_details,
        name='todo_update_details',
    ),
    path('<int:pk>/delete/', todo_views.todo_delete, name='todo_delete'),
]
