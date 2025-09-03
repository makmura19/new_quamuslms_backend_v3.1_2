from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.tap_attendance_group import TapAttendanceGroup
from models.edu_stage_level import EduStageLevel
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    group_id = serializers.CharField(required=True)
    level_id = serializers.CharField(required=True, allow_null=True)
    day = serializers.ChoiceField(choices=["mon", "tue", "wed", "thu", "fri", "sat", "sun"])
    check_in_time = serializers.FloatField(required=True)
    check_out_time = serializers.FloatField(required=True)
    late_after = serializers.FloatField(required=True)
    early_leave_before = serializers.FloatField(required=True)

    class Meta:
        validate_model = {
            "group_id": {
                "field": "_id",
                "model": TapAttendanceGroup(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "level_id": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }


class UpdateSerializer(BaseSerializer):
    level_id = serializers.CharField(required=True, allow_null=True)
    day = serializers.ChoiceField(choices=["mon", "tue", "wed", "thu", "fri", "sat", "sun"])
    check_in_time = serializers.FloatField(required=True)
    check_out_time = serializers.FloatField(required=True)
    late_after = serializers.FloatField(required=True)
    early_leave_before = serializers.FloatField(required=True)

    class Meta:
        validate_model = {
            "level_id": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
