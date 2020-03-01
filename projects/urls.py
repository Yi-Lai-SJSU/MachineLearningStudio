from django.urls import path
from . import views
from .views import ProjectListView

urlpatterns = [
    path('', views.ProjectListView.as_view(), name="projectList"),
    # path('user/(?P<variable_a>(\d+))/(?P<variable_b>(\d+))/$', views.ProjectListView.as_view(), name="projectList"),
    # path('predict', views.predict),
]