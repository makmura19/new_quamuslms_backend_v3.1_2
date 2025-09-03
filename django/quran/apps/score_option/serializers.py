from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.quran_score_category import QuranScoreCategory
from models.quran_score_type import QuranScoreType
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    category_id = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    type_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    score = serializers.IntegerField(required=False, allow_null=True)
    penalty_point = serializers.IntegerField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=True)
    use_parent_score = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "category_id": {
                "field": "_id",
                "model": QuranScoreCategory(),
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
    score = serializers.IntegerField(required=False, allow_null=True)
    penalty_point = serializers.IntegerField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=True)
    use_parent_score = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}
