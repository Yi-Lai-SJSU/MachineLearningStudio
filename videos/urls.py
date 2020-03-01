from django.urls import path
from . import views
from .views import VideoListView

urlpatterns = [
    path('', views.VideoListView.as_view(), name="videoList"),
    # path('user/(?P<variable_a>(\d+))/(?P<variable_b>(\d+))/$', views.ProjectListView.as_view(), name="projectList"),
    # path('predict', views.predict),
]