from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduSubjectData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    name: str
    short_name: str
    sequence: int
    bar_img: Optional[str] = field(default=None)
    thumbnail_img: Optional[str] = field(default=None)
    color: Optional[str] = field(default=None)
    is_catalogue: bool
    is_active: bool


class EduSubjectSchema(Schema):
    name = ma_fields.String(required=True)
    short_name = ma_fields.String(required=True)
    sequence = ma_fields.Integer(required=True)
    bar_img = ma_fields.String(required=False, allow_none=True)
    thumbnail_img = ma_fields.String(required=False, allow_none=True)
    color = ma_fields.String(required=False, allow_none=True)
    is_catalogue = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class EduSubject(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduSubjectData)
    collection_name = "edu_subject"
    schema = EduSubjectSchema
    search = ["name", "short_name"]
    object_class = EduSubjectData
    foreign_key = {}
