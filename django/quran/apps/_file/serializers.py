from helpers.base_serializer import BaseSerializer
from rest_framework import serializers


class CreateSerializer(BaseSerializer):
    file = serializers.FileField()
