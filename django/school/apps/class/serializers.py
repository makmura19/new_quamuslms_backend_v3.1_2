from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.school_teacher import SchoolTeacher
from models.edu_stage_level import EduStageLevel
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    homeroom_id = serializers.CharField(
        required=True, allow_null=True, allow_blank=True
    )
    level_id = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "homeroom_id": {
                "field": "_id",
                "model": SchoolTeacher(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "level_id": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    homeroom_id = serializers.CharField(required=True)
    level_id = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "homeroom_id": {
                "field": "_id",
                "model": SchoolTeacher(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "level_id": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }


class ItemSerializer(serializers.Serializer):
    _id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    teacher_ids = serializers.ListField(child=serializers.CharField(), required=True)
    is_active = serializers.BooleanField(required=True)
    threshold = serializers.IntegerField(required=True)


class UpdateSubjectSerializer(BaseSerializer):
    data = serializers.ListField(child=ItemSerializer(), required=True)

    class Meta:
        validate_model = {}
