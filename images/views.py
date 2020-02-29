from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets
from .serializers import ImageSerializer
from .models import Image
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action

# Create your views here.
class ImageListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return HttpResponse("Get images")

    def post(self, request):
        return HttpResponse("Post Images")

    def put(self, request):
        return HttpResponse("Put Images")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def predict(request):
    return HttpResponse("Image predict")
