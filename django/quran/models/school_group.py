from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolGroupData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    name: str


class SchoolGroupSchema(Schema):
    name = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolGroup(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolGroupData)
    collection_name = "school_group"
    schema = SchoolGroupSchema
    search = ["name"]
    object_class = SchoolGroupData
    foreign_key = {}
