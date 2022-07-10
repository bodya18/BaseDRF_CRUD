from django.contrib import admin
from django.urls import path, include
from todo_api import urls as todo_urls
from user_api import urls as user_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      contact=openapi.Contact(email="contact@contact.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('todos/', include(todo_urls)),
    path('users/', include(user_urls)),
    path('swagger/', schema_view.with_ui(cache_timeout=0), name='schema-json'),
]