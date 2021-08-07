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
    


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now=True)

class IssueLabel(models.Model):
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=7)

class Issue(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    title = models.CharField(max_length=200)
    labels = models.ManyToManyField(IssueLabel, related_name="issues", blank=True)
    creation_date = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now=True)