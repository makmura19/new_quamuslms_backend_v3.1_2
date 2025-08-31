from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class TapTypeData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    activity_id: ObjectId
    code: str
    allow_context: bool
    for_teacher: bool
    for_student: bool


class TapTypeSchema(Schema):
    activity_id = ObjectIdField(required=True, allow_none=False)
    code = ma_fields.String(required=True)
    allow_context = ma_fields.Boolean(required=True)
    for_teacher = ma_fields.Boolean(required=True)
    for_student = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class TapType(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(TapTypeData)
    collection_name = "tap_type"
    schema = TapTypeSchema
    search = ["code"]
    object_class = TapTypeData
    foreign_key = {
        "activity": {
            "local": "activity_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.tap_activity"
            ).tap_activity.TapActivity(),
        }
    }
