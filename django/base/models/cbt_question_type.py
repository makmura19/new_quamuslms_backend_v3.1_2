from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class CbtQuestionTypeData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    code: str
    name: str
    description: str
    is_interactive: bool
    is_auto_graded: bool
    is_active: bool


class CbtQuestionTypeSchema(Schema):
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    is_interactive = ma_fields.Boolean(required=True)
    is_auto_graded = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class CbtQuestionType(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(CbtQuestionTypeData)
    collection_name = "cbt_question_type"
    schema = CbtQuestionTypeSchema
    search = ["code", "name"]
    object_class = CbtQuestionTypeData
    foreign_key = {}
