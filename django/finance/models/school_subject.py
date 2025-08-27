from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolSubjectData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    subject_id: Optional[ObjectId] = field(default=None)
    name: str
    short_name: str
    image: Optional[str] = field(default=None)
    treshold: int
    is_template: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=True)


class SchoolSubjectSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    subject_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    short_name = ma_fields.String(required=True)
    image = ma_fields.String(required=False, allow_none=True)
    treshold = ma_fields.Integer(required=True)
    is_template = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolSubject(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolSubjectData)
    collection_name = "school_subject"
    schema = SchoolSubjectSchema
    search = ["name", "short_name"]
    object_class = SchoolSubjectData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "subject": {
            "local": "subject_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_subject").edu_subject.EduSubject(),
        },
    }
