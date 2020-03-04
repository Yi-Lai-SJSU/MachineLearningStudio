from images.models import Image
import numpy as np
from keras.preprocessing import image
from PIL import Image
from django.contrib.auth.models import User
from projects.models import Project
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.views import APIView
from .serializers import ImageSerializer
from django.http import HttpResponse, JsonResponse
from models.models import Model
from images.models import Image as MyImage
import tensorflow as tf
import os
import datetime

# Create your views here.
class ImageListView(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request):
        user_id = request.GET.get('user_id', '')
        project_title = request.GET.get('project_title', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(title=project_title)
        images = MyImage.objects.filter(user=user, project=project)
        serializer = ImageSerializer(images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        user_id = request.GET.get('user_id', '')
        project_title = request.GET.get('project_title', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(title=project_title, user=user)


:
        label = request.data['type']
        uploaded_files = request.FILES.getlist('files')
        print(label)
        print(uploaded_files)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-"
        print(timestamp)

        image_folder = settings.MEDIA_ROOT + project.location + "images/" + label + "/"
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        fs = FileSystemStorage(location=image_folder)

        index = 0
        for image in uploaded_files:
            image_title = timestamp + str(index) + ".jpg"
            image_path = image_folder + image_title
            fs.save(image_title, image)
            new_image = MyImage(title=image_title,
                                location=project.location + "images/" + label + "/" + image_title,
                                url=settings.MEDIA_URL_DATADASE + project.location + "images/" + label + "/" + image_title,
                                description="default",
                                type=label,
                                user=user,
                                project=project,
                                isTrain=True)
            new_image.save()
            print("Succeed!")
            print(new_image.title)
            index = index + 1
        return HttpResponse("Post Images")

    def put(self, request):
        image_id = request.GET.get('image_id', '')
        image_type = request.GET.get('type', '')
        print(image_id)
        print(image_type)
        image = MyImage.objects.get(id=image_id)
        image.type = image_type
        image.save()
        return HttpResponse("Put Images")

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
class ImagePredict(APIView):
    def post(self, request):
        model_title = request.data['model']
        uploaded_files = request.FILES.getlist('files')
        user_id = request.GET.get('user_id', '')
        project_title = request.GET.get('project_title', '')
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(user_id)
        print(project_title)
        user = User.objects.get(id=user_id)
        project = Project.objects.get(title=project_title)
        print(uploaded_files)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-"
        print(timestamp)

        # https://stackoverflow.com/questions/13821866/queryset-object-has-no-attribute-name
        # model = Model.objects.filter(title=model_title) return a collection
        model = Model.objects.get(title=model_title)
        model_path = settings.MEDIA_ROOT + model.location

        # https://github.com/qubvel/efficientnet/issues/62 to fix ValueError: Unknown activation function:swish
        keras_model = tf.keras.models.load_model(model_path)
        index = 0

        for unPredictedImage in uploaded_files:
            # Get the predict result:
            label_path = settings.MEDIA_ROOT + model.label_location
            label = predictLabel(unPredictedImage, keras_model, label_path, False)

            # Save the image to file-system according to the label:
            image_path = settings.MEDIA_ROOT + project.location + "images/" + label + "/"
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            fs = FileSystemStorage(location=image_path)
            image_title = timestamp + "-" + str(index) + ".jpg"
            fs.save(image_title, unPredictedImage)

            # Save the image to database:
            new_image = MyImage(title=timestamp + "-" + str(index) + ".jpg",
                                location=project.location + "images/" + label + "/" + image_title,
                                url=settings.MEDIA_URL_DATADASE + project.location + "images/" + label + "/" + image_title,
                                description="default",
                                type=label,
                                user=user,
                                project=project,
                                isTrain=True)
            new_image.save()
            index = index + 1

        predictedImage = MyImage.objects.filter(title__startswith=timestamp)
        serializer = ImageSerializer(predictedImage, many=True)
        return JsonResponse(serializer.data, safe=False)

# unpredictedImage: ImageFile, model: keras_model_file, label: path of label.txt;
def predictLabel(unpredictedImage, model, label, imageFormatIsNP):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(type(unpredictedImage))
    # https://stackoverflow.com/questions/22906394/numpy-ndarray-object-has-no-attribute-read
    if imageFormatIsNP:
        test_image = Image.fromarray(unpredictedImage).resize(size=(64, 64))
    else:
        test_image = image.load_img(unpredictedImage, target_size=(64, 64))
        test_image = image.img_to_array(test_image)

    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)
    print(result)
    classIndex = np.argmax(result)
    fr = open(label)
    dic = eval(fr.read())
    fr.close()

    for key in dic:
        if dic[key] == classIndex:
            return key

    return "unknown"
