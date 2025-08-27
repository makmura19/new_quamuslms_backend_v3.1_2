from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class CbtExamParticipantData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    student_id: ObjectId
    exam_id: ObjectId
    log_ids: Optional[List[ObjectId]] = field(default_factory=list)
    state: str
    start_date: Optional[datetime] = field(default=None)
    end_date: Optional[datetime] = field(default=None)
    duration_minutes: float
    is_submitted: bool
    exam_score_id: ObjectId


class CbtExamParticipantSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    student_id = ObjectIdField(required=True, allow_none=False)
    exam_id = ObjectIdField(required=True, allow_none=False)
    log_ids = ma_fields.List(ObjectIdField(), required=True)
    state = ma_fields.String(
        validate=validate.OneOf(["not_started", "in_progress", "submitted", "graded"]),
        required=True,
    )
    start_date = ma_fields.DateTime(required=False, allow_none=True)
    end_date = ma_fields.DateTime(required=False, allow_none=True)
    duration_minutes = ma_fields.Float(required=True)
    is_submitted = ma_fields.Boolean(required=True)
    exam_score_id = ObjectIdField(required=True, allow_none=False)
    _id = ObjectIdField(required=False, allow_none=True)


class CbtExamParticipant(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(CbtExamParticipantData)
    collection_name = "cbt_exam_participant"
    schema = CbtExamParticipantSchema
    search = ["state"]
    object_class = CbtExamParticipantData
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
        "exam": {
            "local": "exam_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.cbt_exam").cbt_exam.CbtExam(),
        },
        "logs": {
            "local": "log_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.ctb_submission_log"
            ).ctb_submission_log.CtbSubmissionLog(),
        },
        "exam_score": {
            "local": "exam_score_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.lms_exam_score"
            ).lms_exam_score.LmsExamScore(),
        },
    }
