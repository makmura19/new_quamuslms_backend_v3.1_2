from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class LmsExamTypeData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    code: str
    name: str
    weight: int
    is_template: bool
    is_report: bool
    is_final: bool
    is_odd_semester: bool
    is_even_semester: bool


class LmsExamTypeSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    weight = ma_fields.Integer(required=True)
    is_template = ma_fields.Boolean(required=True)
    is_report = ma_fields.Boolean(required=True)
    is_final = ma_fields.Boolean(required=True)
    is_odd_semester = ma_fields.Boolean(required=True)
    is_even_semester = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class LmsExamType(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(LmsExamTypeData)
    collection_name = "lms_exam_type"
    schema = LmsExamTypeSchema
    search = ["code", "name"]
    object_class = LmsExamTypeData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        }
    }
