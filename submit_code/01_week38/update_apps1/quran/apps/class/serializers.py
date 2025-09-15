from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.school_teacher import SchoolTeacher
from models.school_student import SchoolStudent
from models.quran_target import QuranTarget
from models.quran_target_group import QuranTargetGroup
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    program_type = serializers.ChoiceField(choices=["tahfidz","tahsin","pra_tahsin"])
    teacher_id = serializers.CharField(required=True)
    teacher_ids = serializers.ListField(child=serializers.CharField(), required=True, allow_empty=True)
    type = serializers.ChoiceField(choices=["regular", "special", "extracurricular"])
    is_target_prerequisite = serializers.BooleanField(required=True)
    target_type = serializers.ChoiceField(choices=["school", "class"])
    use_template = serializers.BooleanField()
    target_group_id = serializers.CharField(required=False, allow_null=True)

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
            "target_group_id": {
                "field": "_id",
                "model": QuranTargetGroup(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
