from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
import json

class ActionPermissions:
     def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            return [permission() for permission in self.permission_classes]

class IssueLabelView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = IssueLabel.objects.all()
    serializer_class = IssueLabelSerializer
    
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
        if "project" in self.request.GET:
            pk = self.request.GET["project"]
            project = get_object_or_404(Project, pk=pk)
            return super().get_queryset().filter(project=project)
        else:
            return super().get_queryset()
    
    serializer_class = IssueSerializer

    @action(detail=False, methods=['post'])
    def set_label(self, request):
        print(request.body)
        post = json.loads(request.body)
        issue_id = post["issue"]
        label_id = post["label"]
        on = post["on"]

        issue : Issue
        issue = get_object_or_404(Issue, pk=issue_id)
        issue_label = get_object_or_404(IssueLabel, pk=label_id)
        
        prefix_of_string = ""
        if issue.labels.filter(pk=label_id).first() == None:
            if on:
                issue.labels.add(issue_label)
                prefix_of_string = "Added label: "
        else:
            if not on:
                issue.labels.remove(issue_label)
                prefix_of_string = "Removed label: "

        Comment.objects.create(
            author = request.user,
            issue = issue,
            body = prefix_of_string + issue_label.name
        )
        
        return Response({
            "success": True
        })

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