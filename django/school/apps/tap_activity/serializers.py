from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    code = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)
    required_tap_count = serializers.IntegerField(required=True, min_value=0)
    is_attendance = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)
    required_tap_count = serializers.IntegerField(required=True, min_value=0)
    is_attendance = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}