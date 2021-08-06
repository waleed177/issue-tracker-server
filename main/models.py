from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    pass

class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class IssueLabel(models.Model):
    name = models.CharField(max_length=64)

class Issue(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    title = models.CharField(max_length=200)
    labels = models.ManyToManyField(IssueLabel, related_name="issues", blank=True)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()