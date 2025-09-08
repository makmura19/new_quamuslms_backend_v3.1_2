from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.edu_stage_level import EduStageLevel
from models.tap_attendance_group import TapAttendanceGroup
from constants.params_validation_type import ParamsValidationType


class ScheduleSerializer(serializers.Serializer):
    day = serializers.ChoiceField(
        choices=["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    )
    is_exists = serializers.BooleanField(required=True)
    check_in_time = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    check_out_time = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    late_after = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    early_leave_before = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class CreateSerializer(BaseSerializer):
    level_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    group_id = serializers.CharField(required=True)
    schedule = ScheduleSerializer(many=True, required=True)

    class Meta:
        validate_model = {
            "level_id": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "group_id": {
                "field": "_id",
                "model": TapAttendanceGroup(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
