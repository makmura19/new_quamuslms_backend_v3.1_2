from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.edu_stage_level import EduStageLevel
from constants.params_validation_type import ParamsValidationType


class ListSerializer(serializers.Serializer):
    gte = serializers.IntegerField(required=True, min_value=0, max_value=100)
    lte = serializers.IntegerField(required=True, min_value=0, max_value=100)
    score = serializers.IntegerField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    level_id = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    name = serializers.CharField(required=True)
    list = ListSerializer(many=True, required=True)
    is_practice = serializers.BooleanField(required=True)
    is_report = serializers.BooleanField(required=True)
    is_group = serializers.BooleanField(required=True)
    is_program = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "level_id": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }
