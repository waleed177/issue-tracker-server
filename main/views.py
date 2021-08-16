#region PREAMBLE
#
#    This is the server-side of the issue-tracker software.
#    Copyright (C) 2021 waleed177 <potatoxel@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, version 3 of the
#    License only.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#endregion

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from . import permissions
import json

class MyPageNumberPagination(PageNumberPagination):
    page_size = 5

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
    permission_classes_by_action = {
        'create': [IsAdminUser],     
        'retrieve': [AllowAny],
        'list': [AllowAny]
    }
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = MyPageNumberPagination


class ProjectIssuesView(ActionPermissions, viewsets.GenericViewSet, 
                        mixins.ListModelMixin, 
                        mixins.RetrieveModelMixin, 
                        mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)

    permission_classes_by_action = {
        'create': [AllowAny],       
        'retrieve': [AllowAny],
        'list': [AllowAny]
    }

    queryset = Issue.objects.all()

    pagination_class = MyPageNumberPagination
    
    def get_queryset(self):
        res = super().get_queryset()
        if "project" in self.request.GET:
            pk = self.request.GET["project"]
            project = get_object_or_404(Project, pk=pk)
            res = res.filter(project=project)
        
        if self.request.user.is_authenticated:
            if "project" in self.request.GET:
                pk = self.request.GET["project"]
                project = get_object_or_404(Project, pk=pk)
                if not self.request.user.is_moderating_project(project):
                    res = res.filter(publicity = Issue.PUBLICITY_PUBLIC)
        else:
            res = res.filter(publicity = Issue.PUBLICITY_PUBLIC)
        
        if "publicity" in self.request.GET:
            res = res.filter(publicity = int(self.request.GET["publicity"]))
        
        if "labels" in self.request.GET:
            labels_str = self.request.GET["labels"]
            if labels_str != "":
                labels = labels_str.split("$")
                query = Q()
                for label in labels:
                    query = query | Q(labels__pk = int(label))
                
                if "include_unlabelled" in self.request.GET:
                    query = query | Q(label_count = 0)
                res = res.annotate(label_count = Count('labels')).filter(query)
            else:
                if "include_unlabelled" in self.request.GET:
                    res = res.annotate(label_count = Count('labels')).filter(label_count = 0)
                else:
                    res = Issue.objects.none()
        

        if "query" in self.request.GET:
            query = self.request.GET["query"]
            res = res.filter(
                Q(title__contains = query)
            )
        return res
        
    
    serializer_class = IssueSerializer

    @action(detail=False, methods=['post'])
    def set_label(self, request):
        post = json.loads(request.body)
        issue_id = post["issue"]
        label_id = post["label"]
        on = post["on"]

        issue : Issue
        issue = get_object_or_404(Issue, pk=issue_id)
        issue_label = get_object_or_404(IssueLabel, pk=label_id)
        
        if not request.user.can_modify_issue_labels(issue, issue_label):
            raise PermissionDenied()

        action = ""
        if issue.labels.filter(pk=label_id).first() == None:
            if on:
                issue.labels.add(issue_label)
                action = "added"
        else:
            if not on:
                issue.labels.remove(issue_label)
                action = "removed"

        if action != "":
            Comment.objects.create(
                author = request.user,
                issue = issue,
                body = json.dumps({
                    "type": "label",
                    "action": action,
                    "label": {
                        "name": issue_label.name,
                        "color": issue_label.color
                    }
                }),
                is_status_change = True
            )
        
        return Response({
            "success": True
        })

    #TODO MAKE PERMISSIONS NOT ALLOW USERS TO WRITE ON CLOSED ISSUE
    #TODO Display a message that the issue is closed
    @action(detail=True, methods=['post'])
    def close_or_open(self, request, pk):
        post = json.loads(request.body)
        issue_id = pk
        open_issue = post["open"]

        issue : Issue
        issue = get_object_or_404(Issue, pk=issue_id)

        if not request.user.can_close_and_open_issues(issue, open_issue):
            raise PermissionDenied()
        
        issue.is_open = open_issue
        issue.save()
        
        Comment.objects.create(
            author = request.user,
            issue = issue,
            body = json.dumps({
                "type": "issue",
                "action": "open" if issue.is_open else "close"
            }),
            is_status_change = True
        )

        return Response(IssueSerializer(issue, context={"request": request}).data)

    
    @action(detail=True, methods=['post'])
    def toggle_publicity(self, request, pk):
        issue_id = pk

        issue : Issue
        issue = get_object_or_404(Issue, pk=issue_id)

        if not request.user.can_modify_publicity(issue):
            raise PermissionDenied()
        
        if issue.publicity == Issue.PUBLICITY_PUBLIC:
            issue.publicity = Issue.PUBLICITY_PRIVATE
        else:
            issue.publicity = Issue.PUBLICITY_PUBLIC
        
        issue.save()

        return Response(IssueSerializer(issue, context={"request": request}).data)


class ProjectIssueCommentsView(ActionPermissions, viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {
        'create': [permissions.CanComment],       
        'retrieve': [permissions.CanComment],
        'list': [permissions.CanReadComments]
    }
    queryset = Comment.objects.all()
    def get_queryset(self):
        pk = self.request.GET["issue"]
        issue = get_object_or_404(Issue, pk=pk)
        return super().get_queryset().filter(issue=issue)
    
    serializer_class = CommentSerializer