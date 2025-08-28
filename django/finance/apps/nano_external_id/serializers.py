from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType
from helpers.custom_serializer_field import DateTimeField


class CreateSerializer(BaseSerializer):
    external_id = serializers.CharField(required=True)

    class Meta:
        validate_model = {}
