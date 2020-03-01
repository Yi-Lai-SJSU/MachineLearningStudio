from django.urls import path
from rest_framework import routers
from . import views
from .views import UserViewSet
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomAuthToken

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('auth/', CustomAuthToken.as_view()),
    path('', include(router.urls)),
]


