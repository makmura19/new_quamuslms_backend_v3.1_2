from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    code = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    preview = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        validate_model = {}
