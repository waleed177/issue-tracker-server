from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    pass

class Project(models.Model):
    name = models.CharField(max_length=100)

class IssueLabel(models.Model):
    name = models.CharField(max_length=64)

class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    title = models.CharField(max_length=200)
    labels = models.ManyToManyField(IssueLabel, related_name="issues", blank=True, null=True)

class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()