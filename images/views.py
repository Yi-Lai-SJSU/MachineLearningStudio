from django.core.files.storage import FileSystemStorage
from images.models import Image
from django.conf import settings
from rest_framework.views import APIView
from .serializers import ImageSerializer
from django.http import HttpResponse, JsonResponse
from models.models import Model
from .models import Image as MyImage
from django.http import HttpResponse
import tensorflow as tf
import numpy as np
from keras.preprocessing import image
import os
import datetime

# Create your views here.
class ImageListView(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request):
        return HttpResponse("Get images")

    def post(self, request):
        return HttpResponse("Post Images")

    def put(self, request):
        return HttpResponse("Put Images")

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
class ImagePredict(APIView):

    def post(self, request):
        model_title = request.data['model']
        uploaded_files = request.FILES.getlist('files')
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(uploaded_files)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-"
        print(timestamp)

        # Get user, project and model
        # user = User.objects.get(id=user_id)
        # project = Project.objects.get(title=project_title, user=user)
        # https://stackoverflow.com/questions/13821866/queryset-object-has-no-attribute-name
        # model = Model.objects.filter(title=model_title) return a collection
        model = Model.objects.get(title=model_title)
        project = model.project
        user=model.user
        model_path = settings.MEDIA_ROOT + model.location

        # https://github.com/qubvel/efficientnet/issues/62 to fix ValueError: Unknown activation function:swish
        keras_model = tf.keras.models.load_model(model_path)
        index = 0
        for unPredictedImage in uploaded_files:
            # Get the predict result:

            print(index)
            print(unPredictedImage)
            test_image = image.load_img(unPredictedImage, target_size=(64, 64))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            result = keras_model.predict(test_image)
            print(result)

            # Get the label of the result
            label = "unknown"
            classIndex = np.argmax(result)
            fr = open(settings.MEDIA_ROOT + model.label_location)
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print(settings.MEDIA_ROOT + model.label_location)
            dic = eval(fr.read())
            print(dic)
            fr.close()

            for key in dic:
                if dic[key] == classIndex:
                    image_path = settings.MEDIA_ROOT + project.location + "images/" + key + "/"
                    print("************************")
                    print(image_path)
                    if not os.path.exists(image_path):
                        os.makedirs(image_path)

                    fs = FileSystemStorage(location=image_path)
                    image_title = timestamp+"-"+str(index)+".jpg"
                    fs.save(image_title, unPredictedImage)

                    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                    new_image = MyImage(title=timestamp+"-"+str(index)+".jpg",
                                        location=project.location + "images/" + str(key) + "/" + image_title,
                                        url=settings.MEDIA_URL_DATADASE + project.location + "images/" + key + "/" + image_title,
                                        description="default",
                                        type=key,
                                        user=user,
                                        project=project,
                                        isTrain=True)
                    new_image.save()
                    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                    index = index + 1

        predictedImage = Image.objects.filter(title__startswith=timestamp)
        serializer = ImageSerializer(predictedImage, many=True)
        return JsonResponse(serializer.data, safe=False)
