from django.contrib import admin
from django.urls import path, include
from todo_api import urls as todo_urls
from user_api import urls as user_urls
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('todos/', include(todo_urls)),
    path('users/', include(user_urls)),
    path('swagger/', schema_view),
]