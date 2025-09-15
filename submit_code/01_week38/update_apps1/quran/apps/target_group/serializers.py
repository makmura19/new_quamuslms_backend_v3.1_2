from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    program_type = serializers.ChoiceField(choices=["tahfidz", "tahsin", "pra_tahsin"])
    name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }