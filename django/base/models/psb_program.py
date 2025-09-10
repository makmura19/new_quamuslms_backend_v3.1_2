from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class PsbProgramData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[str] = field(default=None)
    school_id: ObjectId
    psb_id: ObjectId
    name: str
    slug: str
    academic_year_id: ObjectId
    date_from: datetime
    date_to: datetime
    is_active: bool


class PsbProgramSchema(Schema):
    holding_id = ma_fields.String(required=False, allow_none=True)
    school_id = ObjectIdField(required=True, allow_none=False)
    psb_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    slug = ma_fields.String(required=True)
    academic_year_id = ObjectIdField(required=True, allow_none=False)
    date_from = ma_fields.DateTime(required=True)
    date_to = ma_fields.DateTime(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class PsbProgram(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(PsbProgramData)
    collection_name = "psb_program"
    schema = PsbProgramSchema
    search = ["name", "slug"]
    object_class = PsbProgramData
    foreign_key = {
        "holding": {
            "local": "holding_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, display_name",
            "model": lambda: __import__("models.school_holding").school_holding.SchoolHolding(),
        },
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, code, short_name",
            "model": lambda: __import__("models.school_school").school_school.SchoolSchool(),
        },
        "psb": {
            "local": "psb_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name",
            "model": lambda: __import__("models.psb_psb").psb_psb.PsbPsb(),
        },
        "academic_year": {
            "local": "academic_year_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, year",
            "model": lambda: __import__("models.edu_academic_year").edu_academic_year.EduAcademicYear(),
        },
    }
