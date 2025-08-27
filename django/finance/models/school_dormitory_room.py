from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolDormitoryRoomData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    dormitory_id: ObjectId
    name: str
    student_ids: Optional[List[ObjectId]] = field(default_factory=list)


class SchoolDormitoryRoomSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    dormitory_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    student_ids = ma_fields.List(ObjectIdField(), required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolDormitoryRoom(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolDormitoryRoomData)
    collection_name = "school_dormitory_room"
    schema = SchoolDormitoryRoomSchema
    search = ["name"]
    object_class = SchoolDormitoryRoomData
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
        "dormitory": {
            "local": "dormitory_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_dormitory"
            ).school_dormitory.SchoolDormitory(),
        },
        "student": {
            "local": "student_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student"
            ).school_student.SchoolStudent(),
        },
    }
