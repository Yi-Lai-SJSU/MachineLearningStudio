from django.urls import path
from .views import ImageListView, ImagePredict

urlpatterns = [
    path('', ImageListView.as_view(), name="imageList"),
    path('predict/', ImagePredict.as_view(), name="imagePredict"),
]