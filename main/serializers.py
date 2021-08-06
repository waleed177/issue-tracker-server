from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

class IssueSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ('author',)

class ProjectSerializer(serializers.ModelSerializer):
    #issues = IssueSerializer(many = True, required=False)
    author = UserSerializer(required=False, default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('author',)

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author',)
        