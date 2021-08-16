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

from rest_framework import permissions
from . import models
import json

#more like conditions than permissions.
class CanComment(permissions.BasePermission):
    def has_permission(self, request, view):
        post = json.loads(request.body)
        issue = models.Issue.objects.get(pk=post["issue"])
        return issue.is_open and (
            issue.publicity == issue.PUBLICITY_PUBLIC 
            or not issue.comments.all()
            or request.user.is_moderating_project(issue.project)
        )

class CanReadComments(permissions.BasePermission):
    def has_permission(self, request, view):
        issue = models.Issue.objects.get(pk=request.GET["issue"])
        return (
            issue.is_open and issue.publicity == issue.PUBLICITY_PUBLIC
            or request.user.is_moderating_project(issue.project)
        )


class IsManagingCommentsProject(permissions.BasePermission):
    def has_permission(self, request, view):
        post = json.loads(request.body)
        issue = models.Issue.objects.get(pk=post["issue"])
        return request.user.is_moderating_project(issue.project)