from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from projects.models import Project
from .models import Model
from images.models import Image
from rest_framework import viewsets
from django.core import serializers
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from .models import Model
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import ModelSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from projects.models import Project
from django.db.models import Q

import json
import datetime
import time
import cv2


# Create your views here.
class ModelListView(APIView):
    # permission_classes = (IsAuthenticated, )

    def get(self, request):
        user_id = request.GET.get('user_id', '')
        project_title = request.GET.get('project_title', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(title=project_title)
        # https://my.oschina.net/esdn/blog/834943
        models = Model.objects.filter(
            ((Q(user=user) & Q(project=project)) | Q(isPublic=True)) & Q(type=project.type)
        )

        serializer = ModelSerializer(models, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        print("POST received - return done")
        print(request)
        user_id = request.GET.get('user_id', '')
        project_title = request.GET.get('project_title', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(title=project_title)

        # save to database:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-"
        model = Model(title=timestamp+request.data['title'],
                      description=request.data['description'],
                      type=request.data['type'],
                      isPublic=True,
                      location=project.location + "models/"+timestamp+request.data['title'],
                      url=settings.MEDIA_URL_DATADASE + project.location + "models/" + timestamp + request.data['title'],
                      user=user,
                      project=project)
        model.save()

        # save to file system
        locationOfModels = settings.MEDIA_ROOT + project.location + "models/"
        fs = FileSystemStorage(location=locationOfModels)
        fs.save(timestamp+request.data['title']+".h5", request.data['file'])
        print("**********************")
        return HttpResponse("Upload Models")

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def predict(request):
#     return HttpResponse("Image predict")
