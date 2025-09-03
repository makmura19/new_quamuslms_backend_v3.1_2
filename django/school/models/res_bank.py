from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class ResBankData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    code: str
    name: str
    short_name: str
    image: Optional[str] = field(default=None)
    is_active: bool


class ResBankSchema(Schema):
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    short_name = ma_fields.String(required=True)
    image = ma_fields.String(required=False, allow_none=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ResBank(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ResBankData)
    collection_name = "res_bank"
    schema = ResBankSchema
    search = ["name", "short_name"]
    object_class = ResBankData
    foreign_key = {}
