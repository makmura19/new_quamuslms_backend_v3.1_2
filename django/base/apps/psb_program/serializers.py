from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_holding import SchoolHolding
from models.school_school import SchoolSchool
from models.psb_psb import PsbPsb
from models.edu_academic_year import EduAcademicYear
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    holding_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    school_id = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    psb_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    academic_year_id = serializers.CharField(required=True)
    date_from = serializers.DateTimeField(
        input_formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"],
        required=False,
        allow_null=True,
    )
    date_to = serializers.DateTimeField(
        input_formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"],
        required=False,
        allow_null=True,
    )
    is_active = serializers.BooleanField(required=True)

    def to_internal_value(self, data):
        if data.get("date_from") == "":
            data["date_from"] = None
        if data.get("date_to") == "":
            data["date_to"] = None
        return super().to_internal_value(data)

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
            "academic_year_id": {
                "field": "_id",
                "model": EduAcademicYear(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
