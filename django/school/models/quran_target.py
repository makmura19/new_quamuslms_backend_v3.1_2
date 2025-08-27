from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranTargetData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    group_id: Optional[ObjectId] = field(default=None)
    class_id: Optional[ObjectId] = field(default=None)
    school_id: ObjectId
    name: str
    short_name: str
    program_type: str
    tahfidz_type: Optional[str] = field(default=None)
    juz_id: Optional[ObjectId] = field(default=None)
    chapter_id: Optional[ObjectId] = field(default=None)
    verse_ids: Optional[List[ObjectId]] = field(default_factory=list)
    verse_count: int
    method_id: Optional[ObjectId] = field(default=None)
    book_id: Optional[ObjectId] = field(default=None)
    book_page_from: int
    book_page_to: int
    sequence: int
    is_group: Optional[bool] = field(default=False)
    is_class: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=True)


class QuranTargetSchema(Schema):
    group_id = ObjectIdField(required=False, allow_none=True)
    class_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=True)
    name = ma_fields.String(required=True)
    short_name = ma_fields.String(required=True)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    tahfidz_type = ma_fields.String(
        validate=validate.OneOf([None, "juz", "chapter", "verse", "page", "line"]),
        allow_none=True,
        required=False,
    )
    juz_id = ObjectIdField(required=False, allow_none=True)
    chapter_id = ObjectIdField(required=False, allow_none=True)
    verse_ids = ma_fields.List(ObjectIdField(), required=True)
    verse_count = ma_fields.Integer(required=True)
    method_id = ObjectIdField(required=False, allow_none=True)
    book_id = ObjectIdField(required=False, allow_none=True)
    book_page_from = ma_fields.Integer(required=True)
    book_page_to = ma_fields.Integer(required=True)
    sequence = ma_fields.Integer(required=True)
    is_group = ma_fields.Boolean(required=True)
    is_class = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranTarget(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranTargetData)
    collection_name = "quran_target"
    schema = QuranTargetSchema
    search = ["name", "short_name", "program_type"]
    object_class = QuranTargetData
    foreign_key = {
        "group": {
            "local": "group_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_target_group"
            ).quran_target_group.QuranTargetGroup(),
        },
        "class": {
            "local": "class_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_class").quran_class.QuranClass(),
        },
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
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
        "verses": {
            "local": "verse_ids",
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
