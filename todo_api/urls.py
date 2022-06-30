from django.urls import path, include
from .views import (
    TodoListApiView,
    TodoListAdminApiView,
    TodoDetailApiView
)

urlpatterns = [
    path('api/', TodoListApiView.as_view()),
    path('admin/api/', TodoListAdminApiView.as_view()),
    path('api/<int:todo_id>', TodoDetailApiView.as_view()),
]