from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.views import View
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.conf import settings
import os

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_path = settings.MEDIA_ROOT + "/" + str(user.id)
        print(user_path)
        isExists = os.path.exists(user_path)
        if not isExists:
            os.makedirs(user_path)
            print("succuss")
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
