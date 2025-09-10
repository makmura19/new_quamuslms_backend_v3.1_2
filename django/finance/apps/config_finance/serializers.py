from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType


class ReceiptSerializer(serializers.Serializer):
    header = serializers.CharField(required=True, allow_blank=True)
    place = serializers.CharField(required=True, allow_blank=True)


class CreateSerializer(BaseSerializer):
    sharing_percentage = serializers.IntegerField(required=True)
    daily_pocket_treshold = serializers.IntegerField(required=True, allow_null=True, min_value=0)
    company_fee = serializers.IntegerField(required=True, min_value=0)
    prefix = serializers.CharField(required=True)
    is_auto_debit = serializers.BooleanField(required=True)
    is_pocket_auto_debit = serializers.BooleanField(required=True)
    receipt = ReceiptSerializer(required=True)

    class Meta:
        validate_model = {}
