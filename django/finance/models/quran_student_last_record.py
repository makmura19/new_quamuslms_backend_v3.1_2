from dataclasses import dataclass, field
from typing import Optional, Union
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranStudentLastRecordData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    student_id: ObjectId
    program_type: str
    class_id: ObjectId
    name: str
    notes: Optional[str] = field(default=None)
    chapter_id: Optional[ObjectId] = field(default=None)
    verse_id: Optional[ObjectId] = field(default=None)
    predicate: Optional[str] = field(default=None)
    method_id: Optional[ObjectId] = field(default=None)
    book_id: Optional[ObjectId] = field(default=None)
    book_page: Optional[int] = field(default=None)
    book_page_line: Optional[int] = field(default=None)
    target_seq: int
    target_score: Union[int, float]
    is_ziyadah: bool


class QuranStudentLastRecordSchema(Schema):
    school_id = ObjectIdField(required=True)
    student_id = ObjectIdField(required=True)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    class_id = ObjectIdField(required=True)
    name = ma_fields.String(required=True)
    notes = ma_fields.String(required=False, allow_none=True)
    chapter_id = ObjectIdField(required=False, allow_none=True)
    verse_id = ObjectIdField(required=False, allow_none=True)
    predicate = ma_fields.String(required=False, allow_none=True)
    method_id = ObjectIdField(required=False, allow_none=True)
    book_id = ObjectIdField(required=False, allow_none=True)
    book_page = ma_fields.Integer(required=False, allow_none=True)
    book_page_line = ma_fields.Integer(required=False, allow_none=True)
    target_seq = ma_fields.Integer(required=True)
    target_score = ma_fields.Float(required=True)
    is_ziyadah = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranStudentLastRecord(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranStudentLastRecordData)
    collection_name = "quran_student_last_record"
    schema = QuranStudentLastRecordSchema
    search = ["name", "program_type", "predicate"]
    object_class = QuranStudentLastRecordData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "student": {
            "local": "student_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student"
            ).school_student.SchoolStudent(),
        },
        "class": {
            "local": "class_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_class").quran_class.QuranClass(),
        },
        "chapter": {
            "local": "chapter_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_chapter"
            ).quran_chapter.QuranChapter(),
        },
        "verse": {
            "local": "verse_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_verse").quran_verse.QuranVerse(),
        },
        "method": {
            "local": "method_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.pra_tahsin_method"
            ).pra_tahsin_method.PraTahsinMethod(),
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
