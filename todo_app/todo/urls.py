import todo.views as todo_views
from django.urls import path

# Create your views here.
urlpatterns = [
    path('list/', todo_views.todo_list, name='todo_list'),
    path('todo/<int:pk>/', todo_views.todo_detail, name='todo_detail'),
    path('todo_create/', todo_views.todo_create, name='todo_create'),
    path('submit_todo', todo_views.submit_todo, name='submit_todo'),
]
