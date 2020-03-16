# from __future__ import absolute_import, unicode_literals
# https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/
from celery import Celery
import requests
from .customized import train
import time

app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8');
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

@app.task
def train_mode(user_id, project_title):
    images = load_images(user_id, project_title)
    train(images)

def load_images(user_id, project_title):
    url = 'http://localhost:8000/images/?user_id=' + str(user_id) + '&project_title=' + project_title
    print(url)
    # https://stackoverflow.com/questions/17301938/making-a-request-to-a-restful-api-using-python
    response = requests.get(url)
    print("####################################")
    images = response.json()
    return images
    






