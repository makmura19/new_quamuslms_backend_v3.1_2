from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType
from models.res_bank import ResBank
from models.finance_va_vendor import FinanceVaVendor
from models.school_holding import SchoolHolding
from models.school_school import SchoolSchool


class CreateSerializer(BaseSerializer):
    bank_id = serializers.CharField(required=True)
    vendor_id = serializers.CharField(required=True)
    holding_id = serializers.CharField(required=True, allow_null=True)
    school_id = serializers.CharField(required=True)
    prefix = serializers.CharField(required=True)
    account_no = serializers.CharField(required=True)
    account_name = serializers.CharField(required=True)
    purpose = serializers.ListField(child=serializers.CharField(required=True))
    fee = serializers.IntegerField(required=True)
    partner_id = serializers.CharField(required=True)
    client_id = serializers.CharField(required=True)
    client_secret = serializers.CharField(required=True)
    key = serializers.CharField(required=True)

    class Meta:
        validate_model = {
            "bank_id": {
                "field": "_id",
                "model": ResBank(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "vendor_id": {
                "field": "_id",
                "model": FinanceVaVendor(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "holding_id": {
                "field": "_id",
                "model": SchoolHolding(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID
            }
        }
