from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.edu_degree import EduDegree
from models.edu_stage_group import EduStageGroup
from models.edu_subject import EduSubject
from models.edu_stage_level import EduStageLevel
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    degree_id = serializers.CharField(required=False, allow_null=True)
    group_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    is_final = serializers.BooleanField(required=True)
    is_extension = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "degree_id": {
                "field": "_id",
                "model": EduDegree(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "group_id": {
                "field": "_id",
                "model": EduStageGroup(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "subject_ids": {
                "field": "_id",
                "model": EduSubject(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
        }


class SequenceSerializer(BaseSerializer):
    group_id = serializers.CharField(required=True)
    _ids = serializers.ListField(child=serializers.CharField(), required=True)

    class Meta:
        validate_model = {
            "_ids": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
            "group_id": {
                "field": "_id",
                "model": EduStageGroup(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
