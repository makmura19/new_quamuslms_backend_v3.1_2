from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields

from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranPageData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    juz_id: ObjectId
    juz_seq: int
    name: str
    sequence: int
    verse_count: int
    verse_seq_from: int
    verse_seq_to: int
    line_ids: Optional[List[ObjectId]] = field(default_factory=list)


class QuranPageSchema(Schema):
    juz_id = ObjectIdField(required=True, allow_none=False)
    juz_seq = ma_fields.Integer(required=True)
    name = ma_fields.String(required=True)
    sequence = ma_fields.Integer(required=True)
    verse_count = ma_fields.Integer(required=True)
    verse_seq_from = ma_fields.Integer(required=True)
    verse_seq_to = ma_fields.Integer(required=True)
    line_ids = ma_fields.List(ObjectIdField(), required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranPage(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranPageData)
    collection_name = "quran_page"
    schema = QuranPageSchema
    search = ["name", "sequence"]
    object_class = QuranPageData
    foreign_key = {
        "juz": {
            "local": "juz_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_juz").quran_juz.QuranJuz(),
        },
        "lines": {
            "local": "line_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_line").quran_line.QuranLine(),
        },
    }
