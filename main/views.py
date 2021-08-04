from rest_framework import viewsets, mixins
from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404

# ViewSets define the view behavior.
class ProjectView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectIssuesView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    queryset = Issue.objects.all()

    def get_queryset(self):
        pk = self.request.GET["project"]
        project = get_object_or_404(Project, pk=pk)
        return super().get_queryset().filter(project=project)
    
    serializer_class = IssueSerializer

class ProjectIssueCommentsView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    def get_queryset(self):
        pk = self.request.GET["issue"]
        issue = get_object_or_404(Issue, pk=pk)
        return super().get_queryset().filter(issue=issue)
    serializer_class = CommentSerializer