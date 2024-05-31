import todo.views as todo_views
from django.urls import path

# Create your views here.
urlpatterns = [
    path('list/', todo_views.todo_list, name='todo_list'),
    path('todo/<int:pk>/', todo_views.todo_detail, name='todo_detail'),
]
