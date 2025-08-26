from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from constants.params_validation_type import ParamsValidationType
from helpers.custom_serializer_field import DateTimeField, FileField, FILETYPE


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    staff_no = serializers.CharField(required=True, allow_blank=True)
    resident_no = serializers.CharField(required=True, allow_blank=True)
    birth_date = DateTimeField(allow_null=True)
    birth_place = serializers.CharField(required=True, allow_blank=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    staff_no = serializers.CharField(required=True, allow_blank=True)
    resident_no = serializers.CharField(required=True, allow_blank=True)
    birth_date = DateTimeField(allow_null=True)
    birth_place = serializers.CharField(required=True, allow_blank=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}


class InputXlsSerializer(BaseSerializer):
    school_id = serializers.CharField(required=True)
    file = FileField(required=True, allowed_types=[FILETYPE.XLSX], max_size_mb=15)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }
