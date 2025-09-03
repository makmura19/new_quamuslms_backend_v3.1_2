from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolClassSubjectData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    academic_year_id: ObjectId
    school_id: ObjectId
    class_id: ObjectId
    teacher_ids: Optional[List[ObjectId]] = field(default_factory=list)
    subject_id: ObjectId
    name: str
    threshold: int
    is_sem1_submitted: bool
    is_sem2_submitted: bool
    is_active: bool


class SchoolClassSubjectSchema(Schema):
    academic_year_id = ObjectIdField(required=True, allow_none=False)
    school_id = ObjectIdField(required=True, allow_none=False)
    class_id = ObjectIdField(required=True, allow_none=False)
    teacher_ids = ma_fields.List(ObjectIdField(), required=True)
    subject_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    threshold = ma_fields.Integer(required=True)
    is_sem1_submitted = ma_fields.Boolean(required=True)
    is_sem2_submitted = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolClassSubject(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolClassSubjectData)
    collection_name = "school_class_subject"
    schema = SchoolClassSubjectSchema
    search = ["name"]
    object_class = SchoolClassSubjectData
    foreign_key = {
        "academic_year": {
            "local": "academic_year_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_academic_year"
            ).edu_academic_year.EduAcademicYear(),
        },
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "class": {
            "local": "class_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_class"
            ).school_class.SchoolClass(),
        },
        "teachers": {
            "local": "teacher_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "subject": {
            "local": "subject_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_subject"
            ).school_subject.SchoolSubject(),
        },
    }
