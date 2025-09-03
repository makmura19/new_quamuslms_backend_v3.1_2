from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from constants.params_validation_type import ParamsValidationType
from models.quran_score_category import QuranScoreCategory
from models.quran_score_option import QuranScoreOption


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    name = serializers.CharField(required=True)
    program_type = serializers.ChoiceField(choices=["tahfidz", "tahsin", "pra_tahsin"])
    type = serializers.ChoiceField(
        choices=[None, "numeric", "choice", "multi_choice"], required=False, allow_null=True
    )
    rule = serializers.ChoiceField(
        choices=[None, "accumulative", "average"], required=False, allow_null=True
    )
    min_score = serializers.IntegerField(required=False, allow_null=True)
    max_score = serializers.IntegerField(required=False, allow_null=True)
    is_daily = serializers.BooleanField(required=True)
    is_exam = serializers.BooleanField(required=True)
    is_juziyah = serializers.BooleanField(required=True)
    is_fluency = serializers.BooleanField(required=True)
    is_tajweed = serializers.BooleanField(required=True)
    is_report = serializers.BooleanField(required=True)
    has_category = serializers.BooleanField(required=True)
    category_ids = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    option_ids = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    total_rule = serializers.ChoiceField(
        choices=[None, "accumulative", "average"], required=False, allow_null=True
    )
    penalty_point = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "category_ids": {
                "field": "_id",
                "model": QuranScoreCategory(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
            "option_ids": {
                "field": "_id",
                "model": QuranScoreOption(),
                "type": ParamsValidationType.OBJECT_IDS,
            }
        }
        
        
class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    type = serializers.ChoiceField(
        choices=[None, "numeric", "choice", "multi_choice"], required=False, allow_null=True
    )
    rule = serializers.ChoiceField(
        choices=[None, "accumulative", "average"], required=False, allow_null=True
    )
    min_score = serializers.IntegerField(required=False, allow_null=True)
    max_score = serializers.IntegerField(required=False, allow_null=True)
    is_daily = serializers.BooleanField(required=True)
    is_exam = serializers.BooleanField(required=True)
    is_juziyah = serializers.BooleanField(required=True)
    is_fluency = serializers.BooleanField(required=True)
    is_tajweed = serializers.BooleanField(required=True)
    is_report = serializers.BooleanField(required=True)
    has_category = serializers.BooleanField(required=True)
    category_ids = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    option_ids = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    total_rule = serializers.ChoiceField(
        choices=[None, "accumulative", "average"], required=False, allow_null=True
    )
    penalty_point = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        validate_model = {
            "category_ids": {
                "field": "_id",
                "model": QuranScoreCategory(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
            "option_ids": {
                "field": "_id",
                "model": QuranScoreOption(),
                "type": ParamsValidationType.OBJECT_IDS,
            }
        }
