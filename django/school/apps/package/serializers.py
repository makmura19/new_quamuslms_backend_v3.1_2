from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_subject import SchoolSubject
from models.edu_stage_level import EduStageLevel
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    subject_id = serializers.CharField(required=True)
    level_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    is_public = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "subject_id": {
                "field": "_id",
                "model": SchoolSubject(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "level_id": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
