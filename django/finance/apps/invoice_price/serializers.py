from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.edu_stage_level import EduStageLevel
from constants.params_validation_type import ParamsValidationType


class InvoiceTypeSerializer(serializers.Serializer):
    _id = serializers.CharField(required=True, allow_blank=True)
    is_exists = serializers.BooleanField(required=True)
    amount = serializers.IntegerField(required=True)


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    level_id = serializers.CharField(required=True, allow_blank=True)
    invoice_type = serializers.ListField(child=InvoiceTypeSerializer(), required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "level_id": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }