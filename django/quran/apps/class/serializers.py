from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.school_teacher import SchoolTeacher
from models.school_student import SchoolStudent
from models.quran_target import QuranTarget
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    teacher_id = serializers.CharField(required=True)
    teacher_ids = serializers.ListField(child=serializers.CharField(), required=True, allow_empty=True)
    student_ids = serializers.ListField(child=serializers.CharField(), required=True, allow_empty=True)
    target_ids = serializers.ListField(child=serializers.CharField(), required=True, allow_empty=True)
    type = serializers.ChoiceField(choices=["regular", "special", "extracurricular"])
    is_target_prerequisite = serializers.BooleanField(required=True)
    target_type = serializers.ChoiceField(choices=["school", "class"])

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "teacher_id": {
                "field": "_id",
                "model": SchoolTeacher(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "teacher_ids": {
                "field": "_id",
                "model": SchoolTeacher(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
            "student_ids": {
                "field": "_id",
                "model": SchoolStudent(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
            "target_ids": {
                "field": "_id",
                "model": QuranTarget(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
        }
