from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.config_quran_report import ConfigQuranReport
from models.school_teacher import SchoolTeacher
from constants.params_validation_type import ParamsValidationType
from helpers.custom_serializer_field import PhoneNumberField


class UpdateMeSerializer(BaseSerializer):
    daily_assesment_rule = serializers.ChoiceField(choices=["type_1", "type_2"])
    exam_assesment_rule = serializers.ChoiceField(choices=["type_1", "type_2"])
    juziyah_assesment_rule = serializers.ChoiceField(choices=["type_1", "type_2"])
    coordinator_id = serializers.CharField(required=False, allow_null=True)
    target_period = serializers.ChoiceField(choices=[None, "semester", "year", "full"], allow_null=True)
    exam_threshold = serializers.IntegerField(required=False, allow_null=True)
    use_matrix = serializers.BooleanField(required=True)
    multiple_class_per_student = serializers.BooleanField(required=True)
    use_whatsapp = serializers.BooleanField(required=True)
    whatsapp_no = PhoneNumberField(required=False, allow_null=True, allow_blank=True)
    quran_type = serializers.ChoiceField(choices=["madinah", "kemenag"])

    class Meta:
        validate_model = {
            "report_config_id": {
                "field": "_id",
                "model": ConfigQuranReport(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "coordinator_id": {
                "field": "_id",
                "model": SchoolTeacher(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
