from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class CourseCategoryData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    code: str
    name: str


class CourseCategorySchema(Schema):
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class CourseCategory(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(CourseCategoryData)
    collection_name = "course_category"
    schema = CourseCategorySchema
    search = ["code", "name"]
    object_class = CourseCategoryData
    foreign_key = {}