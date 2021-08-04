from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import *

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    #issues = IssueSerializer(many = True, required=False)
    class Meta:
        model = Project
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'