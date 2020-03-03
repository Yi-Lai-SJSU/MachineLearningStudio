from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Model(models.Model):
    title = models.CharField(max_length=32)
    location = models.TextField(max_length=360)
    label_location = models.TextField(max_length=360, default="")
    url = models.TextField(max_length=360)
    description = models.CharField(max_length=32)
    type = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    isPublic = models.BooleanField(default=True)