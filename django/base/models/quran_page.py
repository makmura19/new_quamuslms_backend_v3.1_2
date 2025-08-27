from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranPageData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    sequence: int
    verse_count: int
    verse_seq_from: int
    verse_seq_to: int
    line_ids: List[ObjectId]


class QuranPageSchema(Schema):
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
    search = ["sequence"]
    object_class = QuranPageData
    foreign_key = {
        "lines": {
            "local": "line_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_line").quran_line.QuranLine(),
        }
    }
