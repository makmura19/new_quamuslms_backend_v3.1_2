from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.school_subject import SchoolSubject
from constants.params_validation_type import ParamsValidationType
from helpers.custom_serializer_field import FileField, FILETYPEGROUP


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    name = serializers.CharField(required=True)
    short_name = serializers.CharField(required=True)
    treshold = serializers.IntegerField(required=True)
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
    short_name = serializers.CharField(required=True)
    treshold = serializers.IntegerField(required=True)
    is_active = serializers.BooleanField(required=True)
    

    class Meta:
        validate_model = {}


class UploadImageSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    file = FileField(
        required=True, allowed_types=[*FILETYPEGROUP.IMAGE], max_size_mb=15
    )

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }


class SequenceSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    _ids = serializers.ListField(child=serializers.CharField(), required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "_ids": {
                "field": "_id",
                "model": SchoolSubject(),
                "type": ParamsValidationType.OBJECT_IDS,
            }
        }
