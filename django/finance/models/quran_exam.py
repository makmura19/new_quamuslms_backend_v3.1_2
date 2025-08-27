from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranExamData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    academic_year_id: ObjectId
    semester_id: ObjectId
    examiner_ids: List[ObjectId]
    class_ids: List[ObjectId]
    date_from: str
    date_to: str
    is_open: bool
    code: str
    name: str
    verse_count: int
    is_score_recap: bool
    is_multiple_submission: bool
    is_entire_verses: bool
    is_shuffle: bool
    content_ids: List[ObjectId]
    program_type: str


class QuranExamSchema(Schema):
    school_id = ObjectIdField(required=True)
    academic_year_id = ObjectIdField(required=True)
    semester_id = ObjectIdField(required=True)
    examiner_ids = ma_fields.List(ObjectIdField(), required=True)
    class_ids = ma_fields.List(ObjectIdField(), required=True)
    date_from = ma_fields.DateTime(required=True)
    date_to = ma_fields.DateTime(required=True)
    is_open = ma_fields.Boolean(required=True)
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    verse_count = ma_fields.Integer(required=True)
    is_score_recap = ma_fields.Boolean(required=True)
    is_multiple_submission = ma_fields.Boolean(required=True)
    is_entire_verses = ma_fields.Boolean(required=True)
    is_shuffle = ma_fields.Boolean(required=True)
    content_ids = ma_fields.List(ObjectIdField(), required=True)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    _id = ObjectIdField(required=False, allow_none=True)


class QuranExam(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranExamData)
    collection_name = "quran_exam"
    schema = QuranExamSchema
    search = ["name", "code", "program_type"]
    object_class = QuranExamData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "academic_year": {
            "local": "academic_year_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_academic_year"
            ).edu_academic_year.EduAcademicYear(),
        },
        "semester": {
            "local": "semester_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_semester"
            ).edu_semester.EduSemester(),
        },
        "examiners": {
            "local": "examiner_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "classes": {
            "local": "class_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_class").quran_class.QuranClass(),
        },
        "contents": {
            "local": "content_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_exam_content"
            ).quran_exam_content.QuranExamContent(),
        },
    }
