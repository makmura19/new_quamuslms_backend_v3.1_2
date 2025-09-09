from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.lms_exam_type import LmsExamType
from models.config_lms_report import ConfigLmsReport
from constants.params_validation_type import ParamsValidationType


class UpdateSerializer(BaseSerializer):
    exam_type_ids = serializers.ListField(
        child=serializers.CharField(), required=True
    )
    config_report_id = serializers.CharField(required=True)
    num_option = serializers.IntegerField(required=True, min_value=0)

    class Meta:
        validate_model = {
            "exam_type_ids": {
                "field": "_id",
                "model": LmsExamType(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
            "config_report_id": {
                "field": "_id",
                "model": ConfigLmsReport(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
