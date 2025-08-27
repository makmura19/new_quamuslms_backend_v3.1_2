from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolDormitoryData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    school_ids: Optional[List[ObjectId]] = field(default_factory=list)
    name: str
    gender: str
    capacity: int
    occupied: Optional[int] = field(default=0)
    staff_ids: Optional[List[ObjectId]] = field(default_factory=list)
    room_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_active: bool


class SchoolDormitorySchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    school_ids = ma_fields.List(ObjectIdField(), required=True)
    name = ma_fields.String(required=True)
    gender = ma_fields.String(
        validate=validate.OneOf(["male", "female"]), required=True
    )
    capacity = ma_fields.Integer(required=True)
    occupied = ma_fields.Integer(required=True)
    staff_ids = ma_fields.List(ObjectIdField(), required=True)
    room_ids = ma_fields.List(ObjectIdField(), required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolDormitory(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolDormitoryData)
    collection_name = "school_dormitory"
    schema = SchoolDormitorySchema
    search = ["name"]
    object_class = SchoolDormitoryData
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
        "schools": {
            "local": "school_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "staffs": {
            "local": "staff_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_staff"
            ).school_staff.SchoolStaff(),
        },
        "rooms": {
            "local": "room_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_dormitory_room"
            ).school_dormitory_room.SchoolDormitoryRoom(),
        },
    }
