from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from constants.params_validation_type import ParamsValidationType
from models.school_teacher import SchoolTeacher
from models.quran_class import QuranClass

class MainFieldSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False, allow_blank=True)
    examiner_ids = serializers.ListField(
        child=serializers.CharField(), required=True, allow_empty=True
    )
    class_ids = serializers.ListField(
        child=serializers.CharField(), required=True, allow_empty=True
    )
    date_from = serializers.DateTimeField(
        input_formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"],
        required=False,
        allow_null=True,
    )
    date_to = serializers.DateTimeField(
        input_formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"],
        required=False,
        allow_null=True,
    )
    is_open = serializers.BooleanField(required=True)
    name = serializers.CharField(required=True)
    is_score_recap = serializers.BooleanField(required=True)
    is_multiple_submission = serializers.BooleanField(required=True)
    is_entire_verses = serializers.BooleanField(required=True)
    is_shuffle = serializers.BooleanField(required=True)
    
    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "examiner_ids": {
                "field": "_id",
                "model": SchoolTeacher(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
            "class_ids": {
                "field": "_id",
                "model": QuranClass(),
                "type": ParamsValidationType.OBJECT_IDS,
            }
        }
    
    
class CreateSerializer(MainFieldSerializer):
    program_type = serializers.ChoiceField(
        choices=["tahfidz", "tahsin", "pra_tahsin"]
    )


class UpdateSerializer(MainFieldSerializer):
    pass