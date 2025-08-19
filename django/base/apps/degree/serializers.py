from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.edu_degree import EduDegree
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    level = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    short_name = serializers.CharField(required=True)
    semester_count = serializers.IntegerField(required=True)

    class Meta:
        validate_model = {}


class SequenceSerializer(BaseSerializer):
    _ids = serializers.ListField(child=serializers.CharField(), required=True)

    class Meta:
        validate_model = {
            "_ids": {
                "field": "_id",
                "model": EduDegree(),
                "type": ParamsValidationType.OBJECT_IDS,
            }
        }
