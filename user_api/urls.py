from django.urls import path, include
from .views import (
    UserListApiView,
    UserListAdminApiView,
    UserDetailApiView
)

urlpatterns = [
    path('api/', UserListApiView.as_view()),
    path('admin/api/', UserListAdminApiView.as_view()),
    path('api/<int:user_id>', UserDetailApiView.as_view()),
]