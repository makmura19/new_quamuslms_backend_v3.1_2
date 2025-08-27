from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranExamStudentData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    academic_year_id: ObjectId
    semester_id: ObjectId
    student_id: ObjectId
    exam_id: ObjectId
    submission_ids: List[ObjectId]
    class_id: ObjectId
    scores: List[Dict[str, Union[str, int, float]]]


class QuranExamStudentSchema(Schema):
    school_id = ObjectIdField(required=True)
    academic_year_id = ObjectIdField(required=True)
    semester_id = ObjectIdField(required=True)
    student_id = ObjectIdField(required=True)
    exam_id = ObjectIdField(required=True)
    submission_ids = ma_fields.List(ObjectIdField(), required=True)
    class_id = ObjectIdField(required=True)
    scores = ma_fields.List(
        ma_fields.Dict(keys=ma_fields.String(), values=ma_fields.Raw()), required=True
    )
    _id = ObjectIdField(required=False, allow_none=True)


class QuranExamStudent(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranExamStudentData)
    collection_name = "quran_exam_student"
    schema = QuranExamStudentSchema
    search = ["scores.name", "scores.rubric_name"]
    object_class = QuranExamStudentData
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
        "student": {
            "local": "student_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student"
            ).school_student.SchoolStudent(),
        },
        "exam": {
            "local": "exam_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_exam").quran_exam.QuranExam(),
        },
        "submissions": {
            "local": "submission_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_submission"
            ).quran_submission.QuranSubmission(),
        },
        "class": {
            "local": "class_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_class").quran_class.QuranClass(),
        },
    }
