from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranExamContentData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    exam_id: ObjectId
    student_id: Optional[ObjectId] = field(default=None)
    sequence: int
    type: str
    is_student: bool
    juz_id: Optional[ObjectId] = field(default=None)
    juz_seq: Optional[int] = field(default=None)
    chapter_id: Optional[ObjectId] = field(default=None)
    chapter_seq: Optional[int] = field(default=None)
    verse_seq_from: Optional[int] = field(default=None)
    verse_seq_to: Optional[int] = field(default=None)
    page_seq_from: Optional[int] = field(default=None)
    page_seq_to: Optional[int] = field(default=None)
    book_id: Optional[ObjectId] = field(default=None)


class QuranExamContentSchema(Schema):
    school_id = ObjectIdField(required=True)
    exam_id = ObjectIdField(required=True)
    student_id = ObjectIdField(required=False, allow_none=True)
    sequence = ma_fields.Integer(required=True)
    type = ma_fields.String(
        validate=validate.OneOf(["juz", "chapter", "page", "custom"]), required=True
    )
    is_student = ma_fields.Boolean(required=True)
    juz_id = ObjectIdField(required=False, allow_none=True)
    juz_seq = ma_fields.Integer(required=False, allow_none=True)
    chapter_id = ObjectIdField(required=False, allow_none=True)
    chapter_seq = ma_fields.Integer(required=False, allow_none=True)
    verse_seq_from = ma_fields.Integer(required=False, allow_none=True)
    verse_seq_to = ma_fields.Integer(required=False, allow_none=True)
    page_seq_from = ma_fields.Integer(required=False, allow_none=True)
    page_seq_to = ma_fields.Integer(required=False, allow_none=True)
    book_id = ObjectIdField(required=False, allow_none=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranExamContent(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranExamContentData)
    collection_name = "quran_exam_content"
    schema = QuranExamContentSchema
    search = ["type", "sequence"]
    object_class = QuranExamContentData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "exam": {
            "local": "exam_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_exam").quran_exam.QuranExam(),
        },
        "student": {
            "local": "student_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student"
            ).school_student.SchoolStudent(),
        },
        "juz": {
            "local": "juz_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_juz").quran_juz.QuranJuz(),
        },
        "chapter": {
            "local": "chapter_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_chapter"
            ).quran_chapter.QuranChapter(),
        },
        "book": {
            "local": "book_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.pra_tahsin_book"
            ).pra_tahsin_book.PraTahsinBook(),
        },
    }
