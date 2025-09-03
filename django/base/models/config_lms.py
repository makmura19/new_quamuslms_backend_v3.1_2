from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class ConfigLmsData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    exam_type_ids: Optional[List[ObjectId]] = field(default_factory=list)
    config_report_id: ObjectId
    num_option: int


class ConfigLmsSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    exam_type_ids = ma_fields.List(ObjectIdField(), required=True)
    config_report_id = ObjectIdField(required=True, allow_none=False)
    num_option = ma_fields.Integer(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ConfigLms(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ConfigLmsData)
    collection_name = "config_lms"
    schema = ConfigLmsSchema
    search = ["school_id"]
    object_class = ConfigLmsData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "exam_types": {
            "local": "exam_type_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.lms_exam_type"
            ).lms_exam_type.LmsExamType(),
        },
        "config_report": {
            "local": "config_report_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.config_lms_report"
            ).config_lms_report.ConfigLmsReport(),
        },
    }
