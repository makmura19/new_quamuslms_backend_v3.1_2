from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranLineData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    sequence: int
    page_id: ObjectId
    page_seq: int
    word_ids: List[ObjectId]
    chapter_name_arabic: str
    chapter_name_latin: str
    last_line: bool
    juz_id: ObjectId
    juz_seq: int
    is_chapter_name: bool


class QuranLineSchema(Schema):
    sequence = ma_fields.Integer(required=True)
    page_id = ObjectIdField(required=True)
    page_seq = ma_fields.Integer(required=True)
    word_ids = ma_fields.List(ObjectIdField(), required=True)
    chapter_name_arabic = ma_fields.String(required=True)
    chapter_name_latin = ma_fields.String(required=True)
    last_line = ma_fields.Boolean(required=True)
    juz_id = ObjectIdField(required=True)
    juz_seq = ma_fields.Integer(required=True)
    is_chapter_name = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranLine(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranLineData)
    collection_name = "quran_line"
    schema = QuranLineSchema
    search = ["chapter_name_arabic", "chapter_name_latin"]
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
