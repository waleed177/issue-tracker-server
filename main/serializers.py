from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import *

class CurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        res = serializer_field.context['request'].user
        if res.is_authenticated:
            return res
        else:
            return None

    def __repr__(self):
        return '%s()' % self.__class__.__name__

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

class IssueLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueLabel
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, default=CurrentUserDefault())
    labels = IssueLabelSerializer(required=False, many=True)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ('author', 'creation_date', 'is_open')

class ProjectSerializer(serializers.ModelSerializer):
    #issues = IssueSerializer(many = True, required=False)
    author = UserSerializer(required=False, default=CurrentUserDefault())
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('author', 'creation_date')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, default=CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'creation_date')
        