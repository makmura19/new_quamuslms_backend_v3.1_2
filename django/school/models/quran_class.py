from dataclasses import dataclass, field
from typing import Optional, List, Union
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranClassData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    academic_year_id: ObjectId
    program_type: str
    name: str
    teacher_id: ObjectId
    teacher_ids: Optional[List[ObjectId]] = field(default_factory=list)
    progress: float
    student_ids: Optional[List[ObjectId]] = field(default_factory=list)
    target_ids: Optional[List[ObjectId]] = field(default_factory=list)
    type: str
    is_target_prerequisite: bool
    target_type: str


class QuranClassSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    academic_year_id = ObjectIdField(required=True, allow_none=False)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    name = ma_fields.String(required=True)
    teacher_id = ObjectIdField(required=True, allow_none=False)
    teacher_ids = ma_fields.List(ObjectIdField(), required=True)
    progress = ma_fields.Float(required=True)
    student_ids = ma_fields.List(ObjectIdField(), required=True)
    target_ids = ma_fields.List(ObjectIdField(), required=True)
    type = ma_fields.String(
        validate=validate.OneOf(["regular", "special", "extracurricular"]),
        required=True,
    )
    is_target_prerequisite = ma_fields.Boolean(required=True)
    target_type = ma_fields.String(
        validate=validate.OneOf(["school", "class"]), required=True
    )
    _id = ObjectIdField(required=False, allow_none=True)


class QuranClass(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranClassData)
    collection_name = "quran_class"
    schema = QuranClassSchema
    search = ["name", "type", "target_type"]
    object_class = QuranClassData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "academic_year": {
            "local": "academic_year_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_academic_year"
            ).edu_academic_year.EduAcademicYear(),
        },
        "teacher": {
            "local": "teacher_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "teachers": {
            "local": "teacher_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "students": {
            "local": "student_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student"
            ).school_student.SchoolStudent(),
        },
        "targets": {
            "local": "target_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_target"
            ).quran_target.QuranTarget(),
        },
    }
