from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolClassSummary:
    male_student_count: int
    female_student_count: int
    subject_count: int


@dataclass(kw_only=True)
class SchoolClassData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    academic_year_id: ObjectId
    name: str
    homeroom_id: ObjectId
    student_ids: Optional[List[ObjectId]] = field(default_factory=list)
    subject_ids: Optional[List[ObjectId]] = field(default_factory=list)
    class_subject_ids: Optional[List[ObjectId]] = field(default_factory=list)
    level_id: ObjectId
    level_sequence: int
    mutabaah_rule_ids: Optional[List[ObjectId]] = field(default_factory=list)
    ignored_mutabaah_rule_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_report_sem1_created: Optional[bool] = field(default=False)
    is_report_sem2_created: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=True)
    summary: Optional[SchoolClassSummary] = field(
        default_factory=lambda: {
            "male_student_count": 0,
            "female_student_count": 0,
            "subject_count": 0,
        }
    )


class SchoolClassSummarySchema(Schema):
    male_student_count = ma_fields.Integer(required=True)
    female_student_count = ma_fields.Integer(required=True)
    subject_count = ma_fields.Integer(required=True)


class SchoolClassSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    academic_year_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    homeroom_id = ObjectIdField(required=True, allow_none=False)
    student_ids = ma_fields.List(ObjectIdField(), required=True)
    subject_ids = ma_fields.List(ObjectIdField(), required=True)
    class_subject_ids = ma_fields.List(ObjectIdField(), required=True)
    level_id = ObjectIdField(required=True, allow_none=False)
    level_sequence = ma_fields.Integer(required=True)
    mutabaah_rule_ids = ma_fields.List(ObjectIdField(), required=True)
    ignored_mutabaah_rule_ids = ma_fields.List(ObjectIdField(), required=True)
    is_report_sem1_created = ma_fields.Boolean(required=True)
    is_report_sem2_created = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    summary = ma_fields.Nested(SchoolClassSummarySchema, required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolClass(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolClassData)
    collection_name = "school_class"
    schema = SchoolClassSchema
    search = ["name"]
    object_class = SchoolClassData
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
        "homeroom": {
            "local": "homeroom_id",
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
        "subjects": {
            "local": "subject_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_subject"
            ).school_subject.SchoolSubject(),
        },
        "class_subjects": {
            "local": "class_subject_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_class_subject"
            ).school_class_subject.SchoolClassSubject(),
        },
        "level": {
            "local": "level_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_level").edu_level.EduLevel(),
        },
        "mutabaah_rules": {
            "local": "mutabaah_rule_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.mutabaah_practice_rule"
            ).mutabaah_practice_rule.MutabaahPracticeRule(),
        },
        "ignored_mutabaah_rules": {
            "local": "ignored_mutabaah_rule_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.mutabaah_practice_rule"
            ).mutabaah_practice_rule.MutabaahPracticeRule(),
        },
    }
