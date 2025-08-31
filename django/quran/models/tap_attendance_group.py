from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class TapAttendanceGroupData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    name: str
    for_student: bool
    for_teacher: bool
    teacher_ids: Optional[List[ObjectId]] = field(default_factory=list)
    schedule_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_default: bool
    is_active: bool


class TapAttendanceGroupSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    for_student = ma_fields.Boolean(required=True)
    for_teacher = ma_fields.Boolean(required=True)
    teacher_ids = ma_fields.List(ObjectIdField(), required=True)
    schedule_ids = ma_fields.List(ObjectIdField(), required=True)
    is_default = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class TapAttendanceGroup(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(TapAttendanceGroupData)
    collection_name = "tap_attendance_group"
    schema = TapAttendanceGroupSchema
    search = ["name"]
    object_class = TapAttendanceGroupData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "teachers": {
            "local": "teacher_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "schedules": {
            "local": "schedule_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.tap_attendance_schedule"
            ).tap_attendance_schedule.TapAttendanceSchedule(),
        },
    }
