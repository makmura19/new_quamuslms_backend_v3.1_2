from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.edu_stage_level import EduStageLevel
from models.mutabaah_practice_rubric import MutabaahPracticeRubric
from constants.params_validation_type import ParamsValidationType


class CustomTargetField(serializers.Field):
    def to_internal_value(self, data):
        if isinstance(data, (str, bool, int)):
            return data
        raise serializers.ValidationError("Input must be a string, boolean, or integer.")

    def to_representation(self, value):
        return value
    

class PracticeSerializer(serializers.Serializer):
    type_id = serializers.CharField(required=True)
    is_exists = serializers.BooleanField(required=True)
    target = CustomTargetField(required=True, allow_null=True)
    weight = serializers.IntegerField(required=True, min_value=0)
    min_score = serializers.IntegerField(required=True, min_value=0)
    max_score = serializers.IntegerField(required=True, min_value=0)


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    level_id = serializers.CharField(required=True)
    practice = PracticeSerializer(many=True, required=True)

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
            },
        }


class OptionSerializer(serializers.Serializer):
    item = serializers.CharField(required=True)
    score = serializers.IntegerField(required=True, min_value=0)


class UpdateSerializer(BaseSerializer):
    type = serializers.ChoiceField(choices=["boolean", "quantitative", "options", "time"])
    options = OptionSerializer(many=True, required=True, allow_empty=True)
    days_of_week = serializers.ListField(child=serializers.IntegerField(min_value=1, max_value=7), required=True, allow_empty=True)
    period = serializers.ChoiceField(choices=["day", "week", "month", "semester", "year"])
    unit = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    interval = serializers.IntegerField(required=True, allow_null=True, min_value=0)
    penalty_per_interval = serializers.IntegerField(required=True, allow_null=True, min_value=0)
    submitted_by = serializers.ChoiceField(choices=["parent", "teacher", "all"])
    rubric_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        validate_model = {
            "rubric_id": {
                "field": "_id",
                "model": MutabaahPracticeRubric(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }

