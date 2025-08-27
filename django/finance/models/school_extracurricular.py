from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolExtracurricularData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    teacher_ids: Optional[List[ObjectId]] = field(default_factory=list)
    name: str
    description: str
    is_active: Optional[bool] = field(default=True)


class SchoolExtracurricularSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    teacher_ids = ma_fields.List(ObjectIdField(), required=True)
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolExtracurricular(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolExtracurricularData)
    collection_name = "school_extracurricular"
    schema = SchoolExtracurricularSchema
    search = ["name", "description"]
    object_class = SchoolExtracurricularData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "teachers": {
            "local": "teacher_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
    }
