from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.edu_stage_group import EduStageGroup
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    group_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    short_name = serializers.CharField(required=True)
    origin = serializers.ChoiceField(
        choices=["domestic", "religion", "vocational", "graduate", "boarding"]
    )

    class Meta:
        validate_model = {
            "group_id": {
                "field": "_id",
                "model": EduStageGroup(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }
