from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.quran_score_type import QuranScoreType
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    type_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    penalty_point = serializers.FloatField(required=True)
    max_score = serializers.IntegerField(required=True)
    min_score = serializers.IntegerField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "type_id": {
                "field": "_id",
                "model": QuranScoreType(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
        
        
class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    penalty_point = serializers.FloatField(required=True)
    max_score = serializers.IntegerField(required=True)
    min_score = serializers.IntegerField(required=True)

    class Meta:
        validate_model = {}
