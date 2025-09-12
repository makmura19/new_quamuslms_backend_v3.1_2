from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_holding import SchoolHolding
from models.school_school import SchoolSchool
from models.psb_psb import PsbPsb
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    holding_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    school_id = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    psb_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    qty = serializers.IntegerField(required=True)
    is_active = serializers.BooleanField()

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
            "psb_id": {
                "field": "_id",
                "model": PsbPsb(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
