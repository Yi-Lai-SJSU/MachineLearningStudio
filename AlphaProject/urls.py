from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('images/', include('images.urls')),
    # path('models/', include('models.urls')),
    # path('projects/', include('projects.urls')),
    path('users/', include('users.urls')),
    # path('videos/', include('videos.urls')),
]
