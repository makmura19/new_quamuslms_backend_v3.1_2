from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType
from helpers.custom_serializer_field import FileField, FILETYPEGROUP


class CreateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)
    program_type = serializers.ChoiceField(choices=["tahfidz", "tahsin", "pra_tahsin"])

    class Meta:
        validate_model = {}


class UploadPreviewSerializer(BaseSerializer):
    file = FileField(
        required=True, allowed_types=[*FILETYPEGROUP.IMAGE], max_size_mb=15
    )

    class Meta:
        validate_model = {}
