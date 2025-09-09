from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.mutabaah_practice_type import MutabaahPracticeType
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    type_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    class Meta:
        validate_model = {
            "type_id": {
                "field": "_id",
                "model": MutabaahPracticeType(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        validate_model = {}
