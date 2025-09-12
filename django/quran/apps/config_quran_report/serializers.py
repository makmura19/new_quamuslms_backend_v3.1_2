from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.quran_report_type import QuranReportType
from constants.params_validation_type import ParamsValidationType


class StudentInfoSerializer(serializers.Serializer):
    academic_class = serializers.BooleanField(required=True)
    quran_class = serializers.BooleanField(required=True)
    teacher = serializers.BooleanField(required=True)
    semester = serializers.BooleanField(required=True)
    academic_year = serializers.BooleanField(required=True)
    nis = serializers.BooleanField(required=True)
    nisn = serializers.BooleanField(required=True)


class HeaderSerializer(serializers.Serializer):
    school_logo = serializers.BooleanField(required=True)
    quamus_logo = serializers.BooleanField(required=True)
    holding_logo = serializers.BooleanField(required=True)
    address = serializers.BooleanField(required=True)
    title = serializers.BooleanField(required=True)
    periodic_title = serializers.BooleanField(required=True)
    academic_year = serializers.BooleanField(required=True)


class SignatureSerializer(serializers.Serializer):
    principal = serializers.BooleanField(required=True)
    coordinator = serializers.BooleanField(required=True)
    parent = serializers.BooleanField(required=True)
    quamus = serializers.BooleanField(required=True)


class LabelSerializer(serializers.Serializer):
    principal = serializers.CharField(required=True, allow_blank=True)
    coordinator = serializers.CharField(required=True, allow_blank=True)
    parent = serializers.CharField(required=True, allow_blank=True)
    title = serializers.CharField(required=True, allow_blank=True)
    periodic_title = serializers.CharField(required=True, allow_blank=True)
    place = serializers.CharField(required=True, allow_blank=True)
    address = serializers.CharField(required=True, allow_blank=True)


class ComponentScoreSerializer(serializers.Serializer):
    is_daily = serializers.BooleanField(required=True)
    is_exam = serializers.BooleanField(required=True)


class ReportRubricSerializer(serializers.Serializer):
    letter = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    gte = serializers.IntegerField(required=True, min_value=0, max_value=100)
    lte = serializers.IntegerField(required=True, min_value=0, max_value=100)


class UpdateMeSerializer(BaseSerializer):
    type_id = serializers.CharField(required=True)
    student_info = StudentInfoSerializer(required=True)
    header = HeaderSerializer(required=True)
    signature = SignatureSerializer(required=True)
    label = LabelSerializer(required=True)
    use_chapter_recap = serializers.BooleanField(required=True)
    total_rule = serializers.ChoiceField(choices=[None, "accumulative", "average"], allow_null=True)
    component_score = ComponentScoreSerializer(required=True)
    report_rubric = ReportRubricSerializer(many=True, required=True)

    class Meta:
        validate_model = {
            "type_id": {
                "field": "_id",
                "model": QuranReportType(),
                "type": ParamsValidationType.OBJECT_ID,
            }
        }
