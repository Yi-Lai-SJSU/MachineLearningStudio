from __future__ import absolute_import, unicode_literals
# from __future__ import absolute_import, unicode_literals
# https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/
# https://ruddra.com/posts/docker-do-stuff-using-celery-using-redis-as-broker/   * main ref
# https://www.revsys.com/tidbits/celery-and-django-and-docker-oh-my/
# https://mopitz199.github.io/docs/celery-redis-django-docker.html

import os
from celery import Celery
import logging
from .customized import train
# from models.customized import train
from django.conf import settings
from django.apps import apps
import datetime

# https://ruddra.com/posts/docker-do-stuff-using-celery-using-redis-as-broker/

logger = logging.getLogger("Celery")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AlphaProject.settings')

app = Celery('celery_tasks.tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def train_mode(param1, param2):
    project_folder = getProjectFolder(param2)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-"
    train(project_folder, timestamp)

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(param2)

    # https://stackoverflow.com/questions/57666355/cannot-import-models-into-celery-tasks-in-django
    # It works well!
    Model = apps.get_model(app_label='models', model_name='model')
    Project = apps.get_model(app_label='projects', model_name='project')
    User = apps.get_model(app_label='auth', model_name='User')
    user = User.objects.get(id=param2[0])
    project = Project.objects.get(user=user, title=param2[1])
    print(user.id)
    print(user.username)
    print(project.title)

    model = Model.objects.create(title=timestamp + "-keras.h5",
                                 location=project.location + "models/" + timestamp + "-keras.h5",
                                 label_location=project.location + "models/" + timestamp + "-classLabel.txt",
                                 url=settings.MEDIA_URL_DATADASE + "models/" + timestamp + "-keras.h5",
                                 description="default",
                                 type=param2[2],
                                 user=user,
                                 project=project,
                                 isPublic=True)
    model.save()

    locationOfModel = os.path.abspath(os.path.dirname(__file__))
    print(locationOfModel)


    return "success"

def getProjectFolder(param2):
    project_folder = settings.MEDIA_ROOT + str(param2[0]) + "/" + param2[1] + "/"
    return project_folder
    






