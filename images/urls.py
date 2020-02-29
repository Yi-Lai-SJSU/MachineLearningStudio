from django.urls import path
from . import views
from .views import ImageListView

urlpatterns = [
    path('', views.ImageListView.as_view(), name="imageList"),
    path('predict', views.predict),
]