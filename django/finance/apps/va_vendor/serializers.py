from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.res_bank import ResBank
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    bank_id = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    short_name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "bank_id": {
                "field": "_id",
                "model": ResBank(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    short_name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}
