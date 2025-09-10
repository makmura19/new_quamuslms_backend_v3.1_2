from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_holding import SchoolHolding
from models.school_school import SchoolSchool
from models.finance_invoice_type import FinanceInvoiceType
from models.psb_psb import PsbPsb
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    holding_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    school_id = serializers.CharField(required=True)
    invoice_type_id = serializers.CharField(required=True)
    month = serializers.ListField(child=serializers.IntegerField(), required=True)
    semester = serializers.ListField(child=serializers.IntegerField(), required=True)
    psb_id = serializers.CharField(required=True)

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
            "invoice_type_id": {
                "field": "_id",
                "model": FinanceInvoiceType(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "psb_id": {
                "field": "_id",
                "model": PsbPsb(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
