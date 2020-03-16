from .models import Video
from django.contrib.auth.models import User
from projects.models import Project
import cv2
from images.views import predictLabel
from images.serializers import ImageSerializer
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.views import APIView
from .serializers import VideoSerializer
from django.http import HttpResponse, JsonResponse
from models.models import Model
from images.models import Image as MyImage
import tensorflow as tf
import os
import datetime


# Create your views here.
class VideoListView(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request):
        user_id = request.GET.get('user_id', '')
        project_title = request.GET.get('project_title', '')
        # print(user_id)
        # print(project_title)
        videos = Video.objects.filter(
            user=User.objects.get(id=user_id),
            project=Project.objects.get(title=project_title)
        )
        # print(videos)
        serializer = VideoSerializer(videos, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        print("POST received - return done")

        # Get all the param
        user_id = request.GET.get('user_id', '')
        project_title = request.GET.get('project_title', '')
        model_title = request.data['model']
        timeF = int(request.data['interval'])
        uploaded_file = request.data['file']

        user = User.objects.get(id=user_id)
        project = Project.objects.get(title=project_title, user=user)
        model = Model.objects.get(title=model_title)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-"

        locationOfVideos = settings.MEDIA_ROOT + project.location + "videos/"
        locationOfFrames = settings.MEDIA_ROOT + project.location + "images/unknown/"

        fs = FileSystemStorage(location=locationOfVideos)
        fs.save(timestamp + uploaded_file.name, uploaded_file)

        videoFile  = locationOfVideos + timestamp + uploaded_file.name
        outputFile = locationOfFrames

        video = Video(title=timestamp + uploaded_file.name,
                      description="default",
                      location=project.location + "videos/" + timestamp + uploaded_file.name,
                      url=settings.MEDIA_URL_DATADASE + project.location + "videos/" + timestamp + uploaded_file.name,
                      type="unknown",
                      user=user,
                      project=project)
        video.save()

        vc = cv2.VideoCapture(videoFile)
        c = 1
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            print('openerror!')
            rval = False

        model_path = settings.MEDIA_ROOT + model.location
        keras_model = tf.keras.models.load_model(model_path)
        label_path = settings.MEDIA_ROOT + model.label_location
        print(model_path)
        
        while rval:
            rval, frame = vc.read()
            if c % timeF == 0:
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                # Predict the class of the frame
                predicted_label = predictLabel(frame, keras_model, label_path, True)
                print(predicted_label)
                print("LOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOG")

                # Get the folder path to save the Frame, if not exited, create a new folder
                image_folder = settings.MEDIA_ROOT + project.location + "images/" + predicted_label + "/"
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)

                # Save the frame to the folder
                image_title = timestamp + str(int(c / timeF)) + '.jpg'
                image_path = image_folder + image_title
                cv2.imwrite(image_path, frame)

                # Save to the Image database
                new_image = MyImage(title=image_title,
                                    location=project.location + "images/" + predicted_label + "/" + image_title,
                                    url=settings.MEDIA_URL_DATADASE + project.location + "images/" + predicted_label + "/" + image_title,
                                    description="default",
                                    type=predicted_label,
                                    user=user,
                                    project=project,
                                    isTrain=True)
                new_image.save()
            c += 1
            cv2.waitKey(1)
        vc.release()

        predictedImage = MyImage.objects.filter(title__startswith=timestamp)
        serializer = ImageSerializer(predictedImage, many=True)
        return JsonResponse(serializer.data, safe=False)
