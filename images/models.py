from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from videos.models import Video

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=32)
    location = models.TextField(max_length=360)
    url = models.TextField(max_length=360)
    description = models.CharField(max_length=32)
    type = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    isTrain = models.BooleanField(default=True)