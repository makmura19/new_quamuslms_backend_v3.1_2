from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.lms_report_type import LmsReportType
from constants.params_validation_type import ParamsValidationType


class StudentInfoSerializer(serializers.Serializer):
    academic_class = serializers.BooleanField(required=True)
    quran_class = serializers.BooleanField(required=True)
    teacher = serializers.BooleanField(required=True)
    semester = serializers.BooleanField(required=True)
    academic_year = serializers.BooleanField(required=True)
    nis = serializers.BooleanField(required=True)
    nisn = serializers.BooleanField(required=True)


class HeaderSerializer(serializers.Serializer):
    school_logo = serializers.BooleanField(required=True)
    quamus_logo = serializers.BooleanField(required=True)
    holding_logo = serializers.BooleanField(required=True)
    address = serializers.BooleanField(required=True)
    title = serializers.BooleanField(required=True)
    periodic_title = serializers.BooleanField(required=True)
    academic_year = serializers.BooleanField(required=True)


class SignatureSerializer(serializers.Serializer):
    principal = serializers.BooleanField(required=True)
    coordinator = serializers.BooleanField(required=True)
    parent = serializers.BooleanField(required=True)
    quamus = serializers.BooleanField(required=True)


class ReportRubricSerializer(serializers.Serializer):
    letter = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    gte = serializers.IntegerField(required=True)
    lte = serializers.IntegerField(required=True)


class CreateSerializer(BaseSerializer):
    type_id = serializers.CharField(required=True)
    student_info = StudentInfoSerializer(required=True)
    header = HeaderSerializer(required=True)
    signature = SignatureSerializer(required=True)
    report_rubric = serializers.ListField(
        child=ReportRubricSerializer(), required=True
    )

    class Meta:
        validate_model = {
            "type_id": {
                "field": "_id",
                "model": LmsReportType(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
