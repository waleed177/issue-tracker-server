from rest_framework import viewsets, mixins
from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

class ActionPermissions:
     def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            return [permission() for permission in self.permission_classes]

# ViewSets define the view behavior.
class ProjectView(ActionPermissions, viewsets.GenericViewSet,
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {'list': [AllowAny]}
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectIssuesView(ActionPermissions, viewsets.GenericViewSet, 
                        mixins.ListModelMixin, 
                        mixins.RetrieveModelMixin, 
                        mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {'list': [AllowAny]}

    queryset = Issue.objects.all()

    def get_queryset(self):
        pk = self.request.GET["project"]
        project = get_object_or_404(Project, pk=pk)
        return super().get_queryset().filter(project=project)
    
    serializer_class = IssueSerializer

class ProjectIssueCommentsView(ActionPermissions, viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {'list': [AllowAny]}

    queryset = Comment.objects.all()
    def get_queryset(self):
        pk = self.request.GET["issue"]
        issue = get_object_or_404(Issue, pk=pk)
        return super().get_queryset().filter(issue=issue)
    
    serializer_class = CommentSerializer