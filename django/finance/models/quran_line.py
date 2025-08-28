from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields

from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranLineChapterNameData:
    latin: str
    arabic: str


@dataclass(kw_only=True)
class QuranLineData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    name: str
    sequence: int
    page_id: ObjectId
    page_seq: int
    word_ids: Optional[List[ObjectId]] = field(default_factory=list)
    chapter_name: QuranLineChapterNameData
    chapter_seq: Optional[int] = field(default=None)
    juz_id: ObjectId
    juz_seq: int
    is_word: bool
    is_title: bool
    is_first_line: bool
    is_last_line: bool


class QuranLineChapterNameSchema(Schema):
    latin = ma_fields.String(required=True)
    arabic = ma_fields.String(required=True)


class QuranLineSchema(Schema):
    name = ma_fields.String(required=True)
    sequence = ma_fields.Integer(required=True)
    page_id = ObjectIdField(required=True, allow_none=False)
    page_seq = ma_fields.Integer(required=True)
    word_ids = ma_fields.List(ObjectIdField(), required=True)
    chapter_name = ma_fields.Nested(QuranLineChapterNameSchema, required=True)
    chapter_seq = ma_fields.Integer(required=False, allow_none=True)
    juz_id = ObjectIdField(required=True, allow_none=False)
    juz_seq = ma_fields.Integer(required=True)
    is_word = ma_fields.Boolean(required=True)
    is_title = ma_fields.Boolean(required=True)
    is_first_line = ma_fields.Boolean(required=True)
    is_last_line = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranLine(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranLineData)
    collection_name = "quran_line"
    schema = QuranLineSchema
    search = ["name", "chapter_name.latin", "chapter_name.arabic"]
    object_class = QuranLineData
    foreign_key = {
        "page": {
            "local": "page_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_page").quran_page.QuranPage(),
        },
        "words": {
            "local": "word_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_word").quran_word.QuranWord(),
        },
        "juz": {
            "local": "juz_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_juz").quran_juz.QuranJuz(),
        },
    }
