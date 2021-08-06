from django.contrib import admin
from . import models

admin.site.register(models.Issue)
admin.site.register(models.Comment)
admin.site.register(models.IssueLabel)
admin.site.register(models.Project)
