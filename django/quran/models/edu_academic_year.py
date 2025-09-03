from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime, timezone

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduAcademicYearData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    name: str
    short_name: str
    year: int
    start_date: datetime
    end_date: datetime
    semester_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_active: bool


class EduAcademicYearSchema(Schema):
    name = ma_fields.String(required=True)
    short_name = ma_fields.String(required=True)
    year = ma_fields.Integer(required=True)
    start_date = ma_fields.DateTime(required=True)
    end_date = ma_fields.DateTime(required=True)
    semester_ids = ma_fields.List(ObjectIdField(), required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class EduAcademicYear(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduAcademicYearData)
    collection_name = "edu_academic_year"
    schema = EduAcademicYearSchema
    search = ["name", "short_name", "year"]
    object_class = EduAcademicYearData
    foreign_key = {
        "semester": {
            "local": "semester_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_semester"
            ).edu_semester.EduSemester(),
        }
    }

    def get_active(self):
        now = datetime.now(timezone.utc)
        academic_year_data = self.find_one(
            {"start_date": {"$lte": now}, "end_date": {"$gte": now}}
        )
        return academic_year_data
