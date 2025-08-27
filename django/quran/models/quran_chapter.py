from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranChapterData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    sequence: int
    name_latin: str
    name_arabic: str
    translation: str
    verse_count: int
    page_from: int
    page_to: int
    verse_seq_from: int
    verse_seq_to: int


class QuranChapterSchema(Schema):
    sequence = ma_fields.Integer(required=True)
    name_latin = ma_fields.String(required=True)
    name_arabic = ma_fields.String(required=True)
    translation = ma_fields.String(required=True)
    verse_count = ma_fields.Integer(required=True)
    page_from = ma_fields.Integer(required=True)
    page_to = ma_fields.Integer(required=True)
    verse_seq_from = ma_fields.Integer(required=True)
    verse_seq_to = ma_fields.Integer(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranChapter(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranChapterData)
    collection_name = "quran_chapter"
    schema = QuranChapterSchema
    search = ["name_latin", "name_arabic", "translation"]
    object_class = QuranChapterData
    foreign_key = {}
