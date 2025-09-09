from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    code = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    weight = serializers.IntegerField(required=True)
    is_template = serializers.BooleanField(required=True)
    is_report = serializers.BooleanField(required=True)
    is_final = serializers.BooleanField(required=True)
    is_odd_semester = serializers.BooleanField(required=True)
    is_even_semester = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    weight = serializers.IntegerField(required=True)
    is_template = serializers.BooleanField(required=True)
    is_report = serializers.BooleanField(required=True)
    is_final = serializers.BooleanField(required=True)
    is_odd_semester = serializers.BooleanField(required=True)
    is_even_semester = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }
