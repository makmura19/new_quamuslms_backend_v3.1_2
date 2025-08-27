from helpers.base_serializer import BaseSerializer
from rest_framework import serializers


class CreateSerializer(BaseSerializer):

    class Meta:
        validate_model = {}


class LoginSerializer(BaseSerializer):
    code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ChangePasswordSerializer(BaseSerializer):
    new_password = serializers.CharField(required=True, max_length=255)
    old_password = serializers.CharField(required=True, max_length=255)
