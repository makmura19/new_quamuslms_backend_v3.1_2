from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_holding import SchoolHolding
from models.school_school import SchoolSchool
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    holding_id = serializers.CharField(required=True, allow_null=True)
    school_id = serializers.CharField(required=True, allow_null=True)
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        validate_model = {
            "holding_id": {
                "field": "_id",
                "model": SchoolHolding(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        validate_model = {}
