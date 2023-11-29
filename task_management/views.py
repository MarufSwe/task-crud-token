from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.cache import cache
from .serializers import TaskSerializer, UserCreateSerializer, UserListSerializer


class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        user = get_user_model().objects.create_user(**serializer.validated_data)

        # Retrieve or create a token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Return the token along with user data
        response_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key,
        }

        # Use appropriate status code based on whether the token was created or retrieved
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        return Response(response_data, status=status_code)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Associate the task with the authenticated user
        serializer.save(user=self.request.user)


# for Cache task list
# class TaskList(generics.ListCreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]
#
#     @cache_page(60 * 15)  # Cache the view for 15 minutes
#     def list(self, request, *args, **kwargs):
#         # Use a cache key that is specific to the authenticated user
#         cache_key = f'task_list_{request.user.id}'
#
#         # Try to get the data from the cache
#         cached_data = cache.get(cache_key)
#
#         if cached_data is None:
#             # If not in the cache, fetch the data and store it in the cache
#             queryset = self.filter_queryset(self.get_queryset())
#             serializer = self.get_serializer(queryset, many=True)
#             cached_data = serializer.data
#             cache.set(cache_key, cached_data)
#
#         return self.get_paginated_response(cached_data)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
