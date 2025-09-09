from rest_framework import serializers
from helpers.base_serializer import BaseSerializer
from models.cbt_question_type import CbtQuestionType
from models.school_subject import SchoolSubject
from models.edu_stage_level import EduStageLevel
from models.edu_chapter import EduChapter
from constants.params_validation_type import ParamsValidationType


class OptionSerializer(serializers.Serializer):
    option = serializers.CharField(required=True)
    is_true = serializers.BooleanField(required=True)


class CreateSerializer(BaseSerializer):
    school_subject_id = serializers.CharField(required=True)
    level_id = serializers.CharField(required=True, allow_null=True)
    chapter_id = serializers.CharField(required=True, allow_null=True)
    difficulty = serializers.ChoiceField(choices=["easy", "medium", "hard"], required=False, allow_null=True)
    text = serializers.CharField(required=True)
    option_list = OptionSerializer(many=True, required=True)
    score = serializers.IntegerField(required=True)
    is_public = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "school_subject_id": {
                "field": "_id",
                "model": SchoolSubject(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "level_id": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "chapter_id": {
                "field": "_id",
                "model": EduChapter(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }


class OptionSerializer2(serializers.Serializer):
    _id = serializers.CharField(required=True, allow_null=True)
    option = serializers.CharField(required=True)
    is_true = serializers.BooleanField(required=True)


class UpdateSerializer(BaseSerializer):
    level_id = serializers.CharField(required=True, allow_null=True)
    chapter_id = serializers.CharField(required=True, allow_null=True)
    difficulty = serializers.ChoiceField(choices=["easy", "medium", "hard"], required=False, allow_null=True)
    text = serializers.CharField(required=True)
    option_list = OptionSerializer2(many=True, required=True)
    score = serializers.IntegerField(required=True)
    is_public = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=True)

    class Meta:
        validate_model = {
            "level_id": {
                "field": "_id",
                "model": EduStageLevel(),
                "type": ParamsValidationType.OBJECT_ID,
            },
            "chapter_id": {
                "field": "_id",
                "model": EduChapter(),
                "type": ParamsValidationType.OBJECT_ID,
            },
        }
