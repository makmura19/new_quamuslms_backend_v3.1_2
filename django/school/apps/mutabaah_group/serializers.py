from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.mutabaah_practice_type import MutabaahPracticeType
from models.mutabaah_practice_rubric import MutabaahPracticeRubric
from models.mutabaah_group import MutabaahGroup
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False)
    name = serializers.CharField(required=True)
    practice_ids = serializers.ListField(
        child=serializers.CharField(), required=True, allow_empty=True
    )
    rubric_id = serializers.CharField(required=False, allow_null=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "practice_ids": {
                "field": "_id",
                "model": MutabaahPracticeType(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
            "rubric_id": {
                "field": "_id",
                "model": MutabaahPracticeRubric(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }

class UpdateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    practice_ids = serializers.ListField(
        child=serializers.CharField(), required=True, allow_empty=True
    )
    rubric_id = serializers.CharField(required=False, allow_null=True)

    class Meta:
        validate_model = {
            "practice_ids": {
                "field": "_id",
                "model": MutabaahPracticeType(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
            "rubric_id": {
                "field": "_id",
                "model": MutabaahPracticeRubric(),
                "type": ParamsValidationType.OBJECT_ID,
            },
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
                "model": MutabaahGroup(),
                "type": ParamsValidationType.OBJECT_IDS,
            }
        }