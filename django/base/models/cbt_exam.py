from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class CbtExamData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    lms_exam_id: ObjectId
    class_ids: Optional[List[ObjectId]] = field(default_factory=list)
    start_date: datetime
    end_date: datetime
    package_id: ObjectId
    duration_minutes: int
    access_token: str
    unlock_token: str
    randomize_question: bool
    randomize_option: bool
    is_open: bool


class CbtExamSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    lms_exam_id = ObjectIdField(required=True, allow_none=False)
    class_ids = ma_fields.List(ObjectIdField(), required=True)
    start_date = ma_fields.DateTime(required=True)
    end_date = ma_fields.DateTime(required=True)
    package_id = ObjectIdField(required=True, allow_none=False)
    duration_minutes = ma_fields.Integer(required=True)
    access_token = ma_fields.String(required=True)
    unlock_token = ma_fields.String(required=True)
    randomize_question = ma_fields.Boolean(required=True)
    randomize_option = ma_fields.Boolean(required=True)
    is_open = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class CbtExam(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(CbtExamData)
    collection_name = "cbt_exam"
    schema = CbtExamSchema
    search = ["access_token", "unlock_token"]
    object_class = CbtExamData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "lms_exam": {
            "local": "lms_exam_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.lms_exam").lms_exam.LmsExam(),
        },
        "school_class": {
            "local": "class_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_class"
            ).school_class.SchoolClass(),
        },
        "cbt_package": {
            "local": "package_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.cbt_package").cbt_package.CbtPackage(),
        },
    }
