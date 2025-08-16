from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolModuleData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    code: str
    name: str
    is_school: bool
    is_holding: bool
    is_active: bool


class SchoolModuleSchema(Schema):
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    is_school = ma_fields.Boolean(required=True)
    is_holding = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolModule(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolModuleData)
    collection_name = "school_module"
    schema = SchoolModuleSchema
    search = ["code", "name"]
    object_class = SchoolModuleData
    foreign_key = {}
