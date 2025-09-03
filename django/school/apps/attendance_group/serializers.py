from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.school_teacher import SchoolTeacher
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    name = serializers.CharField(required=True)
    for_student = serializers.BooleanField(required=False)
    for_teacher = serializers.BooleanField(required=False)
    is_all_teacher = serializers.BooleanField(required=False)
    teacher_ids = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    is_default = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "teacher_ids": {
                "field": "_id",
                "model": SchoolTeacher(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
        }


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    is_all_teacher = serializers.BooleanField(required=False)
    teacher_ids = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )

    class Meta:
        validate_model = {
            "teacher_ids": {
                "field": "_id",
                "model": SchoolTeacher(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
        }

