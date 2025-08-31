from dataclasses import dataclass, field
from typing import Optional, Union
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class TapAttendanceScheduleData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    group_id: ObjectId
    level_id: Optional[ObjectId] = field(default=None)
    day: str
    check_in_time: Union[int, float]
    check_out_time: Union[int, float]
    late_after: Union[int, float]
    early_leave_before: Union[int, float]
    for_student: bool
    for_teacher: bool


class TapAttendanceScheduleSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    group_id = ObjectIdField(required=True, allow_none=False)
    level_id = ObjectIdField(required=False, allow_none=True)
    day = ma_fields.String(
        validate=validate.OneOf(["mon", "tue", "wed", "thu", "fri", "sat", "sun"]),
        required=True,
    )
    check_in_time = ma_fields.Float(required=True)
    check_out_time = ma_fields.Float(required=True)
    late_after = ma_fields.Float(required=True)
    early_leave_before = ma_fields.Float(required=True)
    for_student = ma_fields.Boolean(required=True)
    for_teacher = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class TapAttendanceSchedule(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(TapAttendanceScheduleData)
    collection_name = "tap_attendance_schedule"
    schema = TapAttendanceScheduleSchema
    search = ["day"]
    object_class = TapAttendanceScheduleData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "group": {
            "local": "group_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.tap_attendance_group"
            ).tap_attendance_group.TapAttendanceGroup(),
        },
        "level": {
            "local": "level_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_stage_level"
            ).edu_stage_level.EduStageLevel(),
        },
    }
