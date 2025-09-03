from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.tap_activity import TapActivity
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    activity_id = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    allow_context = serializers.BooleanField(required=True)
    for_teacher = serializers.BooleanField(required=True)
    for_student = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "activity_id": {
                "field": "_id",
                "model": TapActivity(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }


class UpdateSerializer(BaseSerializer):
    allow_context = serializers.BooleanField(required=True)
    for_teacher = serializers.BooleanField(required=True)
    for_student = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}
