from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_holding import SchoolHolding
from models.edu_stage import EduStage
from models.edu_stage_group import EduStageGroup
from models.school_module import SchoolModule
from models.school_group import SchoolGroup
from constants.params_validation_type import ParamsValidationType
from helpers.custom_serializer_field import FileField, FILETYPEGROUP


class AddressSerializer(serializers.Serializer):
    street = serializers.CharField(required=True, allow_blank=True)
    village = serializers.CharField(required=True, allow_blank=True)
    district = serializers.CharField(required=True, allow_blank=True)
    city = serializers.CharField(required=True, allow_blank=True)
    province = serializers.CharField(required=True, allow_blank=True)
    zipcode = serializers.CharField(required=True, allow_blank=True)


class CreateSerializer(BaseSerializer):
    stage_id = serializers.CharField(required=True)
    code = serializers.CharField(required=True, allow_blank=True)
    name = serializers.CharField(required=True)
    npsn = serializers.CharField(required=True, allow_blank=True)
    group_ids = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    tz = serializers.ChoiceField(
        choices=["Asia/Jakarta", "Asia/Makasar", "Asia/Jayapura"]
    )
    address = AddressSerializer(required=True)

    class Meta:
        validate_model = {
            "stage_id": {
                "field": "_id",
                "model": EduStage(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "group_ids": {
                "field": "_id",
                "model": SchoolGroup(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
        }


class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    npsn = serializers.CharField(required=True)
    group_ids = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    address = AddressSerializer(required=True)

    class Meta:
        validate_model = {
            "stage_id": {
                "field": "_id",
                "model": EduStage(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "group_ids": {
                "field": "_id",
                "model": SchoolGroup(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
        }


class ActivateSerializer(BaseSerializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}


class UploadLogoSerializer(BaseSerializer):
    file = FileField(
        required=True, allowed_types=[*FILETYPEGROUP.IMAGE], max_size_mb=15
    )

    class Meta:
        validate_model = {}


class ModuleSerializer(BaseSerializer):
    module_ids = serializers.ListField(child=serializers.CharField(), required=True)

    class Meta:
        validate_model = {
            "module_ids": {
                "field": "_id",
                "model": SchoolModule(),
                "type": ParamsValidationType.OBJECT_IDS,
            }
        }
