from rest_framework import serializers
from helpers.base_serializer import BaseSerializer


class CreateSerializer(BaseSerializer):
    year = serializers.IntegerField(required=True)

    class Meta:
        validate_model = {}
