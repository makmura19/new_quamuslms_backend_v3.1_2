from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.finance_invoice_price import FinanceInvoicePrice
from models.edu_degree import EduDegree
from models.edu_major import EduMajor
from models.edu_program import EduProgram
from constants.params_validation_type import ParamsValidationType


class VariantSerializer(serializers.Serializer):
    gender = serializers.ChoiceField(choices=[None, "male", "female"], allow_null=True)
    is_boarding = serializers.BooleanField(required=True, allow_null=True)
    is_alumni = serializers.BooleanField(required=True, allow_null=True)
    degree_id = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    major_id = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    program_id = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    amount = serializers.IntegerField(required=True)


class CreateSerializer(BaseSerializer):
    invoice_price_id = serializers.CharField(required=True)
    variant = VariantSerializer(many=True, required=True)

    class Meta:
        validate_model = {
            "invoice_price_id": {
                "field": "_id",
                "model": FinanceInvoicePrice(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "degree_id": {
                "field": "_id",
                "model": EduDegree(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "major_id": {
                "field": "_id",
                "model": EduMajor(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "program_id": {
                "field": "_id",
                "model": EduProgram(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
