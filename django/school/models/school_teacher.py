from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolTeacherData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    name: str
    user_id: Optional[ObjectId] = field(default=None)
    login: Optional[str] = field(default=None)
    staff_no: Optional[str] = field(default=None)
    resident_no: Optional[str] = field(default=None)
    birth_date: Optional[datetime] = field(default=None)
    birth_place: Optional[str] = field(default=None)
    is_active: bool


class SchoolTeacherSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    user_id = ObjectIdField(required=False, allow_none=True)
    login = ma_fields.String(required=False, allow_none=True)
    staff_no = ma_fields.String(required=False, allow_none=True)
    resident_no = ma_fields.String(required=False, allow_none=True)
    birth_date = ma_fields.DateTime(required=False, allow_none=True)
    birth_place = ma_fields.String(required=False, allow_none=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolTeacher(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolTeacherData)
    collection_name = "school_teacher"
    schema = SchoolTeacherSchema
    search = ["name", "login", "staff_no", "resident_no"]
    object_class = SchoolTeacherData
    foreign_key = {
        "holding": {
            "local": "holding_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_holding"
            ).school_holding.SchoolHolding(),
        },
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "user": {
            "local": "user_id",
            "foreign": "_id",
            "fields": "_id,login,password",
            "sort": None,
            "model": lambda: __import__("models.res_user").res_user.ResUser(),
        },
    }
