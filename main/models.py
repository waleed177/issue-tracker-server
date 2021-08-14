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

from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    projects_moderating = models.ManyToManyField('Project', 'moderators', blank=True)

    def is_moderating_project(self, project):
        return self.projects_moderating.filter(pk=project.pk).first() != None

    def can_modify_issue_labels(self, issue, label):
        return self.is_moderating_project(issue.project)
    
    def can_close_and_open_issues(self, issue, open):
        return self.is_moderating_project(issue.project)
    
    #Unused
    def can_look_at_issue(self, issue):
        return self.is_moderating_project(issue.project) or issue.publicity == issue.PUBLICITY_PUBLIC

    def can_modify_publicity(self, issue):
        return self.is_moderating_project(issue.project)
     
class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now=True)

class IssueLabel(models.Model):
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=7)

class Issue(models.Model):
    PUBLICITY_PRIVATE = 0
    PUBLICITY_PUBLIC = 1

    PUBLICITY_CHOICES = (
        (PUBLICITY_PRIVATE, 'private'),
        (PUBLICITY_PUBLIC, 'public')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    guest_name = models.CharField(max_length=64, blank=True, null=True)
    publicity = models.IntegerField(choices=PUBLICITY_CHOICES, default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    title = models.CharField(max_length=200)
    labels = models.ManyToManyField(IssueLabel, related_name="issues", blank=True)
    creation_date = models.DateTimeField(auto_now=True)
    is_open = models.BooleanField(default=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    guest_name = models.CharField(max_length=64, blank=True, null=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now=True)
    is_status_change = models.BooleanField(default=False)