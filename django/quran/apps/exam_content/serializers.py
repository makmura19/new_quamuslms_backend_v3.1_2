from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.school_school import SchoolSchool
from models.quran_exam import QuranExam
from models.school_student import SchoolStudent
from models.quran_juz import QuranJuz
from models.quran_chapter import QuranChapter
from models.pra_tahsin_book import PraTahsinBook
from models.quran_exam_content import QuranExamContent
from constants.params_validation_type import ParamsValidationType


class CreateSerializer(BaseSerializer):
    school_id = serializers.CharField(required=False, allow_blank=True)
    exam_id = serializers.CharField(required=True)
    student_id = serializers.CharField(required=False, allow_null=True)
    type = serializers.ChoiceField(choices=["juz", "chapter", "page", "custom"])
    juz_id = serializers.CharField(required=False, allow_null=True)
    chapter_id = serializers.CharField(required=False, allow_null=True)
    verse_seq_from = serializers.IntegerField(required=False, allow_null=True)
    verse_seq_to = serializers.IntegerField(required=False, allow_null=True)
    page_seq_from = serializers.IntegerField(required=False, allow_null=True)
    page_seq_to = serializers.IntegerField(required=False, allow_null=True)
    book_id = serializers.CharField(required=False, allow_null=True)

    class Meta:
        validate_model = {
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "exam_id": {
                "field": "_id",
                "model": QuranExam(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "student_id": {
                "field": "_id",
                "model": SchoolStudent(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "juz_id": {
                "field": "_id",
                "model": QuranJuz(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "chapter_id": {
                "field": "_id",
                "model": QuranChapter(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "book_id": {
                "field": "_id",
                "model": PraTahsinBook(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }


class SequenceSerializer(BaseSerializer):
    exam_id = serializers.CharField(required=True)
    _ids = serializers.ListField(child=serializers.CharField(), required=True)

    class Meta:
        validate_model = {
            "_ids": {
                "field": "_id",
                "model": QuranExamContent(),
                "type": ParamsValidationType.OBJECT_IDS,
            },
            "exam_id": {
                "field": "_id",
                "model": QuranExam(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }