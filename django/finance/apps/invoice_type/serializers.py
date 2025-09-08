from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from constants.params_validation_type import ParamsValidationType
from helpers.custom_serializer_field import DateTimeField, FileField, FILETYPE


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=["month", "semester", "year"])
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)
    due_days = serializers.IntegerField(required=True, min_value=0)
    is_male = serializers.BooleanField(required=True)
    is_female = serializers.BooleanField(required=True)
    is_installment = serializers.BooleanField(required=True)
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
    type = serializers.ChoiceField(choices=["month", "semester", "year"])
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)
    due_days = serializers.IntegerField(required=True, min_value=0)
    is_male = serializers.BooleanField(required=True)
    is_female = serializers.BooleanField(required=True)
    is_installment = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }


class ImportXlsxSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    file = FileField(required=True, allowed_types=[FILETYPE.XLSX], max_size_mb=15)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }
