from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from .models import Project
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import ProjectSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings

# Create your views here.
class ProjectListView(APIView):
    # permission_classes = (IsAuthenticated, )

    def get(self, request):
        user_id = request.GET.get('user_id', '')
        print(user_id)
        projects = Project.objects.filter(user=User.objects.get(id=user_id))
        print(projects)
        serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        print(request.data)
        user_id = request.data['user_id']
        project_title = request.data['title']
        project_description = request.data['description']
        project_type = request.data['type']

        project_path = settings.MEDIA_ROOT + str(user_id) + "/" + project_title + "/"
        print(project_path)
        if not os.path.exists(project_path):
            os.makedirs(project_path)
            video_path = project_path + "videos/"
            os.makedirs(video_path)
            image_path = project_path + "images/"
            os.makedirs(image_path)
            image_default_path = project_path + "images/unknown/"
            os.makedirs(image_default_path)
            model_path = project_path + "models/"
            os.makedirs(model_path)
            project = Project(title=project_title,
                              location=str(user_id) + "/" + project_title + "/",
                              description=project_description,
                              type=project_type,
                              user=User.objects.get(id=user_id)
                              )
            project.save()
        return HttpResponse("Add new project")

    def put(self, request):
        return HttpResponse("Put Images")

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def predict(request):
#     return HttpResponse("Image predict")

