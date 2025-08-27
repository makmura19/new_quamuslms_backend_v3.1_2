from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranReportLineData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    report_id: ObjectId
    group: int
    data: List[str]
    is_additional: Optional[bool] = field(default=True)


class QuranReportLineSchema(Schema):
    school_id = ObjectIdField(required=True)
    report_id = ObjectIdField(required=True)
    group = ma_fields.Integer(required=True)
    data = ma_fields.List(ma_fields.String(), required=True)
    is_additional = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranReportLine(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranReportLineData)
    collection_name = "quran_report_line"
    schema = QuranReportLineSchema
    search = ["group", "data"]
    object_class = QuranReportLineData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "report": {
            "local": "report_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_student_report"
            ).quran_student_report.QuranStudentReport(),
        },
    }
