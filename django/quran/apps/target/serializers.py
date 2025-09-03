from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from constants.params_validation_type import ParamsValidationType
from models.quran_target_group import QuranTargetGroup
from models.quran_class import QuranClass
from models.school_school import SchoolSchool
from models.quran_juz import QuranJuz
from models.quran_chapter import QuranChapter
from models.quran_verse import QuranVerse
from models.pra_tahsin_method import PraTahsinMethod
from models.pra_tahsin_book import PraTahsinBook
from models.quran_target import QuranTarget


class CreateSerializer(BaseSerializer):
    group_id = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    class_id = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    school_id = serializers.CharField(required=True, allow_null = True)
    program_type = serializers.ChoiceField(choices=["tahfidz", "tahsin", "pra_tahsin"])
    tahfidz_type = serializers.ChoiceField(choices=["juz", "chapter", "verse", "page", "line", None], allow_blank=True, allow_null=True)
    juz_id = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    chapter_id = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    verse_ids = serializers.ListField(
        child=serializers.CharField(), required=True, allow_empty=True
    )
    method_id = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    book_id = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    book_page_from = serializers.IntegerField(required=True, allow_null = True)
    book_page_to = serializers.IntegerField(required=True, allow_null = True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "group_id": {
                "field": "_id",
                "model": QuranTargetGroup(),
                "type": ParamsValidationType.OBJECT_ID
            },
            "class_id": {
                "field": "_id",
                "model": QuranClass(),
                "type": ParamsValidationType.OBJECT_ID
            },
            "school_id": {
                "field": "_id",
                "model": SchoolSchool(),
                "type": ParamsValidationType.OBJECT_ID
            },
            "juz_id": {
                "field": "_id",
                "model": QuranJuz(),
                "type": ParamsValidationType.OBJECT_ID
            },
            "chapter_id": {
                "field": "_id",
                "model": QuranChapter(),
                "type": ParamsValidationType.OBJECT_ID
            },
            "verse_ids": {
                "field": "_id",
                "model": QuranVerse(),
                "type": ParamsValidationType.OBJECT_IDS
            },
            "method_id": {
                "field": "_id",
                "model": PraTahsinMethod(),
                "type": ParamsValidationType.OBJECT_ID
            },
            "book_id": {
                "field": "_id",
                "model": PraTahsinBook(),
                "type": ParamsValidationType.OBJECT_ID
            }
        }
        
        
class SequenceSerializer(BaseSerializer):
    _ids = serializers.ListField(child=serializers.CharField(), required=True)
    
    class Meta:
        validate_model = {
            "_id": {
                "field": "_id",
                "model": QuranTarget(),
                "type": ParamsValidationType.OBJECT_IDS
            }
        }
