from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType
from helpers.custom_serializer_field import DateTimeField, FileField, FILETYPE
from models.school_class import SchoolClass
from models.school_school import SchoolSchool
from helpers.custom_serializer_field import FileField, FILETYPEGROUP


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    name = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=["male", "female"])
    nis = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    nisn = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    birth_place = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    birth_date = DateTimeField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    class_id = serializers.CharField(required=False, allow_null=True)
    is_alumni = serializers.BooleanField(required=True)
    is_boarding = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)

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
            }
        }


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=["male", "female"])
    nis = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    nisn = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    birth_place = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    birth_date = DateTimeField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_alumni = serializers.BooleanField(required=True)
    is_boarding = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}


class UploadPhotoSerializer(BaseSerializer):
    file = FileField(
        required=True, allowed_types=[*FILETYPEGROUP.IMAGE], max_size_mb=15
    )

    class Meta:
        validate_model = {}


class InputXlsSerializer(BaseSerializer):
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


class ImportUpdateSerializer(BaseSerializer):
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


class ActivateSerializer(BaseSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}


class UpdatePinSerializer(BaseSerializer):
    pin = serializers.CharField(required=True)

    class Meta:
        validate_model = {}

# class UpdatePinSerializer(BaseSerializer):
#     old_pin = serializers.CharField(required=True)
#     new_pin_1 = serializers.CharField(required=True)
#     new_pin_2 = serializers.CharField(required=True)

#     class Meta:
#         validate_model = {}


class ClassSerializer(BaseSerializer):
    class_id = serializers.CharField(required=True, allow_null=True)

    class Meta:
        validate_model = {
            "class_id": {
                "field": "_id",
                "model": SchoolClass(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }
