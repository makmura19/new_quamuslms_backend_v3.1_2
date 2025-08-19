from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduSemesterData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    academic_year_id: ObjectId
    semester_no: int
    name: str
    start_date: datetime
    end_date: datetime


class EduSemesterSchema(Schema):
    academic_year_id = ObjectIdField(required=True, allow_none=False)
    semester_no = ma_fields.Integer(required=True)
    name = ma_fields.String(required=True)
    start_date = ma_fields.DateTime(required=True)
    end_date = ma_fields.DateTime(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class EduSemester(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduSemesterData)
    collection_name = "edu_semester"
    schema = EduSemesterSchema
    search = ["name", "semester_no"]
    object_class = EduSemesterData
    foreign_key = {
        "academic_year": {
            "local": "academic_year_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_academic_year"
            ).edu_academic_year.EduAcademicYear(),
        }
    }
