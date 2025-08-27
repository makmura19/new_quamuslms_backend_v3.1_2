from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranJuzData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    sequence: int
    chapter_ids: List[ObjectId]
    verse_seq_from: int
    verse_seq_to: int
    page_seq_from: int
    page_seq_to: int
    verse_count: int


class QuranJuzSchema(Schema):
    sequence = ma_fields.Integer(required=True)
    chapter_ids = ma_fields.List(ObjectIdField(), required=True)
    verse_seq_from = ma_fields.Integer(required=True)
    verse_seq_to = ma_fields.Integer(required=True)
    page_seq_from = ma_fields.Integer(required=True)
    page_seq_to = ma_fields.Integer(required=True)
    verse_count = ma_fields.Integer(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranJuz(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranJuzData)
    collection_name = "quran_juz"
    schema = QuranJuzSchema
    search = ["sequence"]
    object_class = QuranJuzData
    foreign_key = {
        "chapters": {
            "local": "chapter_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_chapter"
            ).quran_chapter.QuranChapter(),
        }
    }
