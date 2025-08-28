from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType
from helpers.custom_serializer_field import FileField, FILETYPEGROUP


class CreateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    short_name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}


class UploadImageSerializer(BaseSerializer):
    file = FileField(
        required=True, allowed_types=[*FILETYPEGROUP.IMAGE], max_size_mb=15
    )

    class Meta:
        validate_model = {}
