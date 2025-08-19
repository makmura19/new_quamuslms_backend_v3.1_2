from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.res_authority import ResAuthority
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
    code = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    address = AddressSerializer(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {}


class UploadLogoSerializer(BaseSerializer):
    file = FileField(
        required=True, allowed_types=[*FILETYPEGROUP.IMAGE], max_size_mb=15
    )

    class Meta:
        validate_model = {}


class StaffSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    role_id = serializers.CharField(required=True)

    class Meta:
        validate_model = {
            "role_id": {
                "field": "_id",
                "model": ResAuthority(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }
