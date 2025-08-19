from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    origin = serializers.ChoiceField(choices=["vocational", "graduate"])
    name = serializers.CharField(required=True)
    short_name = serializers.CharField(required=True)

    class Meta:
        validate_model = {}
