from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from constants.params_validation_type import ParamsValidationType


class MainFieldSerializer(BaseSerializer):
    school_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    gte = serializers.IntegerField(required=True)
    lte = serializers.IntegerField(required=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }


class CreateSerializer(MainFieldSerializer):
    program_type = serializers.ChoiceField(choices=["tahfidz", "tahsin", "pra_tahsin"])
    
    
class UpdateSerializer(MainFieldSerializer):
    pass