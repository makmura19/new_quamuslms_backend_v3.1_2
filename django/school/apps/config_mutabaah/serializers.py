from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType


class UpdateMeSerializer(BaseSerializer):
    use_group = serializers.CharField(required=True)
    use_class = serializers.CharField(required=True)
    score_format = serializers.ChoiceField(choices=["letter", "number"])

    class Meta:
        validate_model = {}
