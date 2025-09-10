from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType
from models.school_holding import SchoolHolding
from models.school_school import SchoolSchool
from models.school_staff import SchoolStaff


class CreateSerializer(BaseSerializer):
    holding_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    school_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    staff_ids = serializers.ListField(
        child=serializers.CharField(), required=True
    )
    name = serializers.CharField(required=True)
    fee = serializers.IntegerField(required=True)
    
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
            "staff_ids": {
                "field": "_id",
                "model": SchoolStaff(),
                "type": ParamsValidationType.OBJECT_IDS
            }
        }