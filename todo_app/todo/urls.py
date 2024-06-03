import todo.views as todo_views
from django.urls import path

# Create your views here.
urlpatterns = [
    path('', todo_views.todo_list, name='todo_list'),
    path('<int:pk>/', todo_views.todo_detail, name='todo_detail'),
    path('create/', todo_views.todo_create, name='todo_create'),
    path('submit/', todo_views.todo_submit, name='todo_submit'),
    path('<int:pk>/edit/', todo_views.todo_edit, name='todo_edit'),
    path('<int:pk>/update/', todo_views.todo_update, name='todo_update'),
    path('<int:pk>/delete/', todo_views.todo_delete, name='todo_delete'),
]
