from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.school_dormitory import SchoolDormitory
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    dormitory_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "dormitory_id": {
                "field": "_id",
                "model": SchoolDormitory(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        validate_model = {}
