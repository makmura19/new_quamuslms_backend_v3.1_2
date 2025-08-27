from dataclasses import dataclass, field
from typing import Optional, List, Union, Dict, Any
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranSubmissionData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    academic_year_id: ObjectId
    semester_id: ObjectId
    class_id: ObjectId
    student_id: ObjectId
    teacher_id: ObjectId
    is_ziyadah: bool
    is_notification: bool
    is_sent: bool
    date: str
    verse_seq_from: Optional[int] = field(default=None)
    verse_seq_to: Optional[int] = field(default=None)
    program_type: str
    rule: Optional[str] = field(default=None)
    scores: List[Dict[str, Any]] = field(default_factory=list)
    target_progress: Optional[Union[int, float]] = field(default=None)
    is_daily: bool = field(default=False)
    is_exam: bool = field(default=False)
    is_juziyah: bool = field(default=False)
    book_id: Optional[ObjectId] = field(default=None)
    page: Dict[str, Any] = field(default_factory=dict)
    list: List[str] = field(default_factory=list)
    correction_list: List[Dict[str, Any]] = field(default_factory=list)
    exam_id: Optional[ObjectId] = field(default=None)
    is_score_recap: bool
    is_join: bool


class QuranSubmissionSchema(Schema):
    school_id = ObjectIdField(required=True)
    academic_year_id = ObjectIdField(required=True)
    semester_id = ObjectIdField(required=True)
    class_id = ObjectIdField(required=True)
    student_id = ObjectIdField(required=True)
    teacher_id = ObjectIdField(required=True)
    is_ziyadah = ma_fields.Boolean(required=True)
    is_notification = ma_fields.Boolean(required=True)
    is_sent = ma_fields.Boolean(required=True)
    date = ma_fields.DateTime(required=True)
    verse_seq_from = ma_fields.Integer(required=False, allow_none=True)
    verse_seq_to = ma_fields.Integer(required=False, allow_none=True)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    rule = ma_fields.String(
        validate=validate.OneOf([None, "type_1", "type_2"]),
        required=False,
        allow_none=True,
    )
    scores = ma_fields.List(
        ma_fields.Dict(
            keys=ma_fields.String(),
            values=ma_fields.Raw(),
        ),
        required=True,
    )
    target_progress = ma_fields.Float(required=False, allow_none=True)
    is_daily = ma_fields.Boolean(required=True)
    is_exam = ma_fields.Boolean(required=True)
    is_juziyah = ma_fields.Boolean(required=True)
    book_id = ObjectIdField(required=False, allow_none=True)
    page = ma_fields.Dict(required=True)
    list = ma_fields.List(ma_fields.String(), required=True)
    correction_list = ma_fields.List(
        ma_fields.Dict(keys=ma_fields.String(), values=ma_fields.Raw()), required=True
    )
    exam_id = ObjectIdField(required=False, allow_none=True)
    is_score_recap = ma_fields.Boolean(required=True)
    is_join = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranSubmission(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranSubmissionData)
    collection_name = "quran_submission"
    schema = QuranSubmissionSchema
    search = ["program_type", "rule", "list"]
    object_class = QuranSubmissionData
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
        "class": {
            "local": "class_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_class").quran_class.QuranClass(),
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
        "book": {
            "local": "book_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.pra_tahsin_book"
            ).pra_tahsin_book.PraTahsinBook(),
        },
        "exam": {
            "local": "exam_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_exam").quran_exam.QuranExam(),
        },
    }
