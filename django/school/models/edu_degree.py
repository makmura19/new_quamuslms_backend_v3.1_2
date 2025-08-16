from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduDegreeData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    level: str
    name: str
    short_name: str
    semester_count: int
    sequence: int


class EduDegreeSchema(Schema):
    level = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    short_name = ma_fields.String(required=True)
    semester_count = ma_fields.Integer(required=True)
    sequence = ma_fields.Integer(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class EduDegree(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduDegreeData)
    collection_name = "edu_degree"
    schema = EduDegreeSchema
    search = ["level", "name", "short_name"]
    object_class = EduDegreeData
    foreign_key = {}
