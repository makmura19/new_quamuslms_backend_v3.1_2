from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranPresenceData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    student_id: Optional[ObjectId] = field(default=None)
    teacher_id: Optional[ObjectId] = field(default=None)
    academic_year_id: ObjectId
    semester_id: ObjectId
    class_id: Optional[ObjectId] = field(default=None)
    date: str
    status: str
    notes: str
    program_type: str
    is_student: Optional[bool] = field(default=False)
    is_teacher: Optional[bool] = field(default=False)


class QuranPresenceSchema(Schema):
    school_id = ObjectIdField(required=True)
    student_id = ObjectIdField(required=False, allow_none=True)
    teacher_id = ObjectIdField(required=False, allow_none=True)
    academic_year_id = ObjectIdField(required=True)
    semester_id = ObjectIdField(required=True)
    class_id = ObjectIdField(required=False, allow_none=True)
    date = ma_fields.DateTime(required=True)
    status = ma_fields.String(
        validate=validate.OneOf(
            [
                "present_and_action",
                "present_only",
                "sick",
                "permission",
                "no_information",
            ]
        ),
        required=True,
    )
    notes = ma_fields.String(required=True)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    is_student = ma_fields.Boolean(required=True)
    is_teacher = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranPresence(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranPresenceData)
    collection_name = "quran_presence"
    schema = QuranPresenceSchema
    search = ["status", "program_type", "notes"]
    object_class = QuranPresenceData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "student": {
            "local": "student_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student"
            ).school_student.SchoolStudent(),
        },
        "teacher": {
            "local": "teacher_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "academic_year": {
            "local": "academic_year_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_academic_year"
            ).edu_academic_year.EduAcademicYear(),
        },
        "semester": {
            "local": "semester_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_semester"
            ).edu_semester.EduSemester(),
        },
        "class": {
            "local": "class_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_class").quran_class.QuranClass(),
        },
    }
