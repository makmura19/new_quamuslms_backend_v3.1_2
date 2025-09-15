from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.school_class import SchoolClass
from models.finance_invoice_type import FinanceInvoiceType
from models.edu_academic_year import EduAcademicYear
from models.edu_semester import EduSemester
from models.school_student import SchoolStudent
from constants.params_validation_type import ParamsValidationType


class StudentSerializer(serializers.Serializer):
    _id = serializers.CharField(required=True)
    student_id = serializers.CharField(required=True)
    student_name = serializers.CharField(required=True)
    student_nis = serializers.CharField(required=True, allow_blank=True)
    amount = serializers.IntegerField(required=True)
    variant_id = serializers.CharField(required=False, allow_null=True)
    is_exists = serializers.BooleanField(required=True)
    is_checked = serializers.BooleanField(required=True)


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=True)
    class_id = serializers.CharField(required=True)
    type_id = serializers.CharField(required=True)
    academic_year_id = serializers.CharField(required=True)
    semester = serializers.IntegerField(required=False, allow_null=True, min_value=1, max_value=2)
    month = serializers.IntegerField(required=False, allow_null=True)
    student = StudentSerializer(many=True, required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "class_id": {
                "field": "_id",
                "model": SchoolClass(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "type_id": {
                "field": "_id",
                "model": FinanceInvoiceType(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "academic_year_id": {
                "field": "_id",
                "model": EduAcademicYear(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "semester_id": {
                "field": "_id",
                "model": EduSemester(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }

