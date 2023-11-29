from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserListSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'token']

    def get_token(self, obj):
        # Retrieve or create a token for the user
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at']
