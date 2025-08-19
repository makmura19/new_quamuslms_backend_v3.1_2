from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.edu_academic_year import EduAcademicYear
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    academic_year_id = serializers.CharField(required=True)
    semester_no = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    start_date = serializers.DateTimeField(
        input_formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"],
        required=False,
        allow_null=True,
    )
    end_date = serializers.DateTimeField(
        input_formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"],
        required=False,
        allow_null=True,
    )

    def to_internal_value(self, data):
        if data.get("start_date") == "":
            data["start_date"] = None
        if data.get("end_date") == "":
            data["end_date"] = None
        return super().to_internal_value(data)

    class Meta:
        validate_model = {
            "academic_year_id": {
                "field": "_id",
                "model": EduAcademicYear(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }
