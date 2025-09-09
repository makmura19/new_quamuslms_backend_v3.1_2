from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.mutabaah_practice_rubric import MutabaahPracticeRubric
from constants.params_validation_type import ParamsValidationType


class OptionSerializer(serializers.Serializer):
    item = serializers.CharField(required=True)
    score = serializers.IntegerField(required=True, min_value=0)


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)
    type = serializers.ChoiceField(choices=["boolean", "quantitative", "options", "time"])
    unit = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    period = serializers.ChoiceField(choices=["day", "week", "month", "semester", "year"])
    interval = serializers.IntegerField(required=True, allow_null=True, min_value=0)
    penalty_per_interval = serializers.IntegerField(required=True, allow_null=True, min_value=0)
    options = OptionSerializer(many=True, required=True, allow_empty=True)
    days_of_week = serializers.ListField(child=serializers.IntegerField(min_value=1, max_value=7), required=True, allow_empty=True)
    gender = serializers.ChoiceField(choices=["male", "female", "all"])
    mandatory_type = serializers.ChoiceField(choices=["wajib", "sunah"])
    submitted_by = serializers.ChoiceField(choices=["parent", "teacher", "all"])
    rubric_id = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    is_mandatory_shalat = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "rubric_id": {
                "field": "_id",
                "model": MutabaahPracticeRubric(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)
    type = serializers.ChoiceField(choices=["boolean", "quantitative", "options", "time"])
    unit = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    period = serializers.ChoiceField(choices=["day", "week", "month", "semester", "year"])
    interval = serializers.IntegerField(required=True, allow_null=True, min_value=0)
    penalty_per_interval = serializers.IntegerField(required=True, allow_null=True, min_value=0)
    options = OptionSerializer(many=True, required=True, allow_empty=True)
    days_of_week = serializers.ListField(child=serializers.IntegerField(min_value=1, max_value=7), required=True, allow_empty=True)
    gender = serializers.ChoiceField(choices=["male", "female", "all"])
    mandatory_type = serializers.ChoiceField(choices=["wajib", "sunah"])
    submitted_by = serializers.ChoiceField(choices=["parent", "teacher", "all"])
    rubric_id = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    is_mandatory_shalat = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "rubric_id": {
                "field": "_id",
                "model": MutabaahPracticeRubric(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }