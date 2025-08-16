from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolFacultyData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    name: str


class SchoolFacultySchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolFaculty(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolFacultyData)
    collection_name = "school_faculty"
    schema = SchoolFacultySchema
    search = ["name"]
    object_class = SchoolFacultyData
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
