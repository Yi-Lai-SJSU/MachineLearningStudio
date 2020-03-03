from rest_framework import serializers
from .models import Model

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'title', 'location', 'label_location', 'description', 'url', 'type', 'user', 'project', 'isPublic')