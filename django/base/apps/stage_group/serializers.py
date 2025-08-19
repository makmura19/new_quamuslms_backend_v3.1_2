from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True)
    has_degree = serializers.BooleanField(required=True)
    has_faculty = serializers.BooleanField(required=True)
    has_subject_mapping = serializers.BooleanField(required=True)
    has_major = serializers.BooleanField(required=True)
    has_program_type = serializers.BooleanField(required=True)
    duration_years = serializers.IntegerField(required=True)
    student_label = serializers.CharField(required=True)

    class Meta:
        validate_model = {}
