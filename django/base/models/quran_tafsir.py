from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranTafsirData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    code: str
    name: str
    is_active: bool


class QuranTafsirSchema(Schema):
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranTafsir(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranTafsirData)
    collection_name = "quran_tafsir"
    schema = QuranTafsirSchema
    search = ["code", "name"]
    object_class = QuranTafsirData
    foreign_key = {}
