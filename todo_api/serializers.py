from rest_framework import serializers
from .models import Todo
from user_api.serializers import UserSerializer


class TodoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Todo
        fields = ["id", "task", "completed", "timestamp", "updated", "user"]