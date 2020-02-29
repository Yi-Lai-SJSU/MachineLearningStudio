from rest_framework import serializers
from .models import Model

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'title', 'description', 'url', 'type', 'users', 'projects')