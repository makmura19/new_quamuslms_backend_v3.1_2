from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    sort_name = serializers.CharField(required=True)
    is_default = serializers.BooleanField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)

    class Meta:
        validate_model = {}
