from django.urls import path
from . import views
from .views import ModelListView

urlpatterns = [
    path('', views.ModelListView.as_view(), name="modelList"),
    # path('user/(?P<variable_a>(\d+))/(?P<variable_b>(\d+))/$', views.ProjectListView.as_view(), name="projectList"),
    # path('predict', views.predict),
]