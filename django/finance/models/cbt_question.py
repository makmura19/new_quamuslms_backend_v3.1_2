from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class CbtQuestionData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    teacher_id: ObjectId
    type_id: ObjectId
    school_subject_id: ObjectId
    edu_subject_id: Optional[ObjectId] = field(default=None)
    level_id: Optional[ObjectId] = field(default=None)
    chapter_id: Optional[ObjectId] = field(default=None)
    difficulty: Optional[str] = field(default=None)
    text: str
    option_ids: Optional[List[ObjectId]] = field(default_factory=list)
    answer_id: Optional[ObjectId] = field(default=None)
    answer_ids: Optional[List[ObjectId]] = field(default_factory=list)
    score: int
    is_public: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=True)


class CbtQuestionSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    teacher_id = ObjectIdField(required=True, allow_none=False)
    type_id = ObjectIdField(required=True, allow_none=False)
    school_subject_id = ObjectIdField(required=True, allow_none=False)
    edu_subject_id = ObjectIdField(required=False, allow_none=True)
    level_id = ObjectIdField(required=False, allow_none=True)
    chapter_id = ObjectIdField(required=False, allow_none=True)
    difficulty = ma_fields.String(
        validate=validate.OneOf([None, "easy", "medium", "hard"]),
        required=False,
        allow_none=True,
    )
    text = ma_fields.String(required=True)
    option_ids = ma_fields.List(ObjectIdField(), required=True)
    answer_id = ObjectIdField(required=False, allow_none=True)
    answer_ids = ma_fields.List(ObjectIdField(), required=True)
    score = ma_fields.Integer(required=True)
    is_public = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class CbtQuestion(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(CbtQuestionData)
    collection_name = "cbt_question"
    schema = CbtQuestionSchema
    search = ["text"]
    object_class = CbtQuestionData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "teacher": {
            "local": "teacher_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "type": {
            "local": "type_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.cbt_question_type"
            ).cbt_question_type.CbtQuestionType(),
        },
        "school_subject": {
            "local": "school_subject_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_subject"
            ).school_subject.SchoolSubject(),
        },
        "edu_subject": {
            "local": "edu_subject_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_subject").edu_subject.EduSubject(),
        },
        "level": {
            "local": "level_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_stage_level"
            ).edu_stage_level.EduStageLevel(),
        },
        "chapter": {
            "local": "chapter_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_chapter").edu_chapter.EduChapter(),
        },
        "options": {
            "local": "option_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.cbt_question_option"
            ).cbt_question_option.CbtQuestionOption(),
        },
        "answer": {
            "local": "answer_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.cbt_question_option"
            ).cbt_question_option.CbtQuestionOption(),
        },
        "answers": {
            "local": "answer_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.cbt_question_option"
            ).cbt_question_option.CbtQuestionOption(),
        },
    }
