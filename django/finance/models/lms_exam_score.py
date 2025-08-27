from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class LmsExamScoreData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    academic_year_id: ObjectId
    semester_id: ObjectId
    exam_type_id: ObjectId
    student_id: ObjectId
    class_id: ObjectId
    exam_id: ObjectId
    subject_id: ObjectId
    teacher_id: ObjectId
    score: int
    notes: str
    url: Optional[str] = field(default=None)
    answer: Optional[str] = field(default=None)
    is_cbt: bool
    participant_id: Optional[ObjectId] = field(default=None)
    activity_id: Optional[ObjectId] = field(default=None)


class LmsExamScoreSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    academic_year_id = ObjectIdField(required=True, allow_none=False)
    semester_id = ObjectIdField(required=True, allow_none=False)
    exam_type_id = ObjectIdField(required=True, allow_none=False)
    student_id = ObjectIdField(required=True, allow_none=False)
    class_id = ObjectIdField(required=True, allow_none=False)
    exam_id = ObjectIdField(required=True, allow_none=False)
    subject_id = ObjectIdField(required=True, allow_none=False)
    teacher_id = ObjectIdField(required=True, allow_none=False)
    score = ma_fields.Integer(required=True)
    notes = ma_fields.String(required=True)
    url = ma_fields.String(required=False, allow_none=True)
    answer = ma_fields.String(required=False, allow_none=True)
    is_cbt = ma_fields.Boolean(required=True)
    participant_id = ObjectIdField(required=False, allow_none=True)
    activity_id = ObjectIdField(required=False, allow_none=True)
    _id = ObjectIdField(required=False, allow_none=True)


class LmsExamScore(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(LmsExamScoreData)
    collection_name = "lms_exam_score"
    schema = LmsExamScoreSchema
    search = ["student_id", "exam_id"]
    object_class = LmsExamScoreData
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
        "exam_type": {
            "local": "exam_type_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_exam_type"
            ).edu_exam_type.EduExamType(),
        },
        "student": {
            "local": "student_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student"
            ).school_student.SchoolStudent(),
        },
        "class": {
            "local": "class_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_class"
            ).school_class.SchoolClass(),
        },
        "exam": {
            "local": "exam_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.lms_exam").lms_exam.LmsExam(),
        },
        "subject": {
            "local": "subject_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_subject"
            ).school_subject.SchoolSubject(),
        },
        "teacher": {
            "local": "teacher_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "participant": {
            "local": "participant_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.cbt_exam_participant"
            ).cbt_exam_participant.CbtExamParticipant(),
        },
        "activity": {
            "local": "activity_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.lms_activity"
            ).lms_activity.LmsActivity(),
        },
    }
