from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduExamTypeData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    code: str
    name: str
    sequence: int
    is_final: bool
    is_deleted: bool


class EduExamTypeSchema(Schema):
    _id = ObjectIdField(required=False, allow_none=True)
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    sequence = ma_fields.Integer(required=True)
    is_final = ma_fields.Boolean(required=True)
    is_deleted = ma_fields.Boolean(required=True)


class EduExamType(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduExamTypeData)
    collection_name = "edu_exam_type"
    schema = EduExamTypeSchema
    search = ["code", "name"]
    object_class = EduExamTypeData
    foreign_key = {}
