from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "email")
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validation_data):
        user = User.objects.create_user(**validation_data)
        token = Token.objects.create(user=user)
        print(token)
        return user