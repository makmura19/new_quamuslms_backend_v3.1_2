from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduProgramData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    name: str
    sort_name: str
    is_default: bool
    description: str


class EduProgramSchema(Schema):
    name = ma_fields.String(required=True)
    sort_name = ma_fields.String(required=True)
    is_default = ma_fields.Boolean(required=True)
    description = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class EduProgram(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduProgramData)
    collection_name = "edu_program"
    schema = EduProgramSchema
    search = ["name", "sort_name", "description"]
    object_class = EduProgramData
    foreign_key = {}
