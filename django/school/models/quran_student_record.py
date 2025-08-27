from dataclasses import dataclass, field
from typing import Optional, List, Union
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class RecordDataItem:
    type: str
    sequence: int
    name: str
    progress: Union[int, float]
    ratio: List[int]
    list: List[str]
    is_completed: bool


class RecordDataItemSchema(Schema):
    type = ma_fields.String(
        validate=validate.OneOf(["juz", "chapter", "book", "page"]), required=True
    )
    sequence = ma_fields.Integer(required=True)
    name = ma_fields.String(required=True)
    progress = ma_fields.Float(required=True)
    ratio = ma_fields.List(ma_fields.Integer(), required=True)
    list = ma_fields.List(ma_fields.String(), required=True)
    is_completed = ma_fields.Boolean(required=True)


@dataclass(kw_only=True)
class RecordSummaryData:
    completed_juz_count: int
    completed_chapter_count: int
    ongoing_juz_count: int
    ongoing_chapter_count: int
    juz_progress: Union[int, float]
    completed_book_count: int


class RecordSummarySchema(Schema):
    completed_juz_count = ma_fields.Integer(required=True)
    completed_chapter_count = ma_fields.Integer(required=True)
    ongoing_juz_count = ma_fields.Integer(required=True)
    ongoing_chapter_count = ma_fields.Integer(required=True)
    juz_progress = ma_fields.Float(required=True)
    completed_book_count = ma_fields.Integer(required=True)


@dataclass(kw_only=True)
class QuranStudentRecordData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    student_id: ObjectId
    data: List[RecordDataItem]
    summary: RecordSummaryData
    program_type: str


class QuranStudentRecordSchema(Schema):
    school_id = ObjectIdField(required=True)
    student_id = ObjectIdField(required=True)
    data = ma_fields.List(ma_fields.Nested(RecordDataItemSchema), required=True)
    summary = ma_fields.Nested(RecordSummarySchema, required=True)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    _id = ObjectIdField(required=False, allow_none=True)


class QuranStudentRecord(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranStudentRecordData)
    collection_name = "quran_student_record"
    schema = QuranStudentRecordSchema
    search = ["student_id", "program_type"]
    object_class = QuranStudentRecordData
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
    }
