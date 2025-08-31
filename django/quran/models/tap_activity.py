from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class TapActivityData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    code: str
    name: str
    description: str
    required_tap_count: int
    type_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_attendance: bool


class TapActivitySchema(Schema):
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    required_tap_count = ma_fields.Integer(required=True)
    type_ids = ma_fields.List(ObjectIdField(), required=True)
    is_attendance = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class TapActivity(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(TapActivityData)
    collection_name = "tap_activity"
    schema = TapActivitySchema
    search = ["code", "name"]
    object_class = TapActivityData
    foreign_key = {
        "types": {
            "local": "type_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.tap_type").tap_type.TapType(),
        }
    }
