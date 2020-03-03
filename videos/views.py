from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from projects.models import Project
from .models import Video
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
from .models import Video
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import VideoSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from projects.models import Project
from models.models import Model

import json
import datetime
import time
import cv2

# Create your views here.
class VideoListView(APIView):
    # permission_classes = (IsAuthenticated, )

    def get(self, request):
        user_id = request.GET.get('user_id', '')
        project_title = request.GET.get('project_title', '')
        # print(user_id)
        # print(project_title)
        videos = Video.objects.filter(
            user=User.objects.get(id=user_id),
            project=Project.objects.get(title=project_title)
        )
        # print(videos)
        serializer = VideoSerializer(videos, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        print("POST received - return done")

        # Get all the param
        user_id = request.GET.get('user_id', '')
        project_title = request.GET.get('project_title', '')
        model_title = request.data['model']
        timeF = int(request.data['interval'])
        uploaded_file = request.data['file']

        user = User.objects.get(id=user_id)
        project = Project.objects.get(title=project_title, user=user)
        model = Model.objects.filter(title=model_title)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-"


        locationOfVideos = settings.MEDIA_ROOT + project.location + "videos/"
        locationOfFrames = settings.MEDIA_ROOT + project.location + "images/unknown/"

        fs = FileSystemStorage(location=locationOfVideos)
        fs.save(timestamp + uploaded_file.name, uploaded_file)

        videoFile  = locationOfVideos + timestamp + uploaded_file.name
        outputFile = locationOfFrames

        video = Video(title=timestamp + uploaded_file.name,
                      description="default",
                      location=project.location + "videos/" + timestamp + uploaded_file.name,
                      url=settings.MEDIA_URL_DATADASE + project.location + "videos/" + timestamp + uploaded_file.name,
                      type="unknown",
                      user=user,
                      project=project)
        video.save()

        vc = cv2.VideoCapture(videoFile)
        c = 1
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            print('openerror!')
            rval = False

        while rval:
            rval, frame = vc.read()
            if c % timeF == 0:
                # print(2)
                cv2.imwrite(outputFile + timestamp + str(int(c / timeF)) + '.jpg', frame)
                image = Image(title=timestamp + str(int(c / timeF)) + '.jpg',
                              location=project.location + "images/unknown/" + timestamp + str(int(c / timeF)) + '.jpg',
                              url=settings.MEDIA_URL_DATADASE + project.location + "images/unknown/" + timestamp + str(int(c / timeF)) + '.jpg',
                              description="default",
                              type="unknown",
                              user=user,
                              project=project,
                              video=video,
                              isTrain=True)
                image.save()
            c += 1
            cv2.waitKey(1)
        vc.release()

        unclassifiedImages = Image.objects.filter(type="unknown", project=project, video=video)
        json_list = []
        for image in unclassifiedImages:
            json_dict = {}
            json_dict['id'] = image.id
            json_dict['title'] = image.title
            json_dict['url'] = image.url
            json_dict['description'] = image.description
            json_list.append(json_dict)
        return HttpResponse(json.dumps(json_list), content_type="application/json")

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def predict(request):
#     return HttpResponse("Image predict")
