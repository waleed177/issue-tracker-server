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

class CanModifyPublicity:
    requires_context = True

    def __call__(self, serializer_field):
        res = serializer_field.context['request'].user
        if res.is_authenticated:
            return res.can_modify_publicity()
        else:
            return False

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
    can_modify_publicity = serializers.SerializerMethodField()
    
    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ('author', 'creation_date', 'is_open', 'publicity', 'can_modify_publicity')

    def get_can_modify_publicity(self, instance):
        request = self.context.get('request')
        user = request.user
        return user.is_authenticated and user.can_modify_publicity(instance)

class ProjectSerializer(serializers.ModelSerializer):
    #issues = IssueSerializer(many = True, required=False)
    author = UserSerializer(required=False, default=CurrentUserDefault())
    is_project_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('author', 'creation_date')

    def get_is_project_admin(self, instance):
        request = self.context.get('request')
        user = request.user
        return user.is_authenticated and user.is_moderating_project(instance)

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, default=CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'creation_date')
        