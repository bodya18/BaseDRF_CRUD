from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import UserSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class UserListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_QUERY, description="This is user identificator", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        users = User.objects.filter(id = request.user.id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('username', openapi.IN_QUERY, description="This is user name", type=openapi.TYPE_STRING),
        openapi.Parameter('password', openapi.IN_QUERY, description="This is user password", type=openapi.TYPE_STRING),
        openapi.Parameter('email', openapi.IN_QUERY, description="This is user email", type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'username': request.data.get('username'), 
            'password': make_password(request.data.get('password')), 
            'email': request.data.get('email')
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsSuperUser, )
    password = serializers.CharField(write_only=True)
    def get_object(self, user_id):
        '''
        Helper method to get the object with given user_id
        '''
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, user_id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('username', openapi.IN_QUERY, description="This is new user name", type=openapi.TYPE_STRING),
        openapi.Parameter('password', openapi.IN_QUERY, description="This is new user password", type=openapi.TYPE_STRING),
        openapi.Parameter('email', openapi.IN_QUERY, description="This is new user email", type=openapi.TYPE_STRING),
        ]
    )
    def put(self, request, user_id, *args, **kwargs):
        '''
        Updates the user
        '''
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'username': request.data.get('username'), 
            'password': make_password(request.data.get('password')), 
            'email': request.data.get('email')
        }
        serializer = UserSerializer(instance = user_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, user_id, *args, **kwargs):
        '''
        Deletes the user
        '''
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        user_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class UserListAdminApiView(APIView):
    permission_classes = (IsSuperUser, )

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all users
        '''
        todos = User.objects.all()
        serializer = UserSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
