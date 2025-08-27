from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class LmsActivityData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    academic_year_id: ObjectId
    semester_id: ObjectId
    class_ids: Optional[List[ObjectId]] = field(default_factory=list)
    repository_id: Optional[ObjectId] = field(default=None)
    teacher_id: ObjectId
    date: datetime
    name: str
    description: str
    exam_id: Optional[ObjectId] = field(default=None)
    state: str
    submit_type: Optional[str] = field(default=None)
    is_exam: bool
    is_assignment: bool
    is_media: bool
    is_active: Optional[bool] = field(default=True)


class LmsActivitySchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    academic_year_id = ObjectIdField(required=True, allow_none=False)
    semester_id = ObjectIdField(required=True, allow_none=False)
    class_ids = ma_fields.List(ObjectIdField(), required=True)
    repository_id = ObjectIdField(required=False, allow_none=True)
    teacher_id = ObjectIdField(required=True, allow_none=False)
    date = ma_fields.DateTime(required=True)
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    exam_id = ObjectIdField(required=False, allow_none=True)
    state = ma_fields.String(
        validate=validate.OneOf(["draft", "publish"]), required=True
    )
    submit_type = ma_fields.String(
        validate=validate.OneOf([None, "text", "url", "manual"]),
        required=False,
        allow_none=True,
    )
    is_exam = ma_fields.Boolean(required=True)
    is_assignment = ma_fields.Boolean(required=True)
    is_media = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class LmsActivity(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(LmsActivityData)
    collection_name = "lms_activity"
    schema = LmsActivitySchema
    search = ["name", "state"]
    object_class = LmsActivityData
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
        "semester": {
            "local": "semester_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_semester"
            ).edu_semester.EduSemester(),
        },
        "classes": {
            "local": "class_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_class"
            ).school_class.SchoolClass(),
        },
        "repository": {
            "local": "repository_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_repository"
            ).school_repository.SchoolRepository(),
        },
        "teacher": {
            "local": "teacher_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "exam": {
            "local": "exam_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.lms_exam").lms_exam.LmsExam(),
        },
    }
