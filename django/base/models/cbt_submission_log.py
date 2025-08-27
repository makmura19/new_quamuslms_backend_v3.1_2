from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class CbtSubmissionLogData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    student_id: ObjectId
    participant_id: ObjectId
    exam_id: ObjectId
    question_id: ObjectId
    selected_option_id: Optional[ObjectId] = field(default=None)
    selected_option_ids: Optional[List[ObjectId]] = field(default_factory=list)
    score: int
    is_correct: bool


class CbtSubmissionLogSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    student_id = ObjectIdField(required=True, allow_none=False)
    participant_id = ObjectIdField(required=True, allow_none=False)
    exam_id = ObjectIdField(required=True, allow_none=False)
    question_id = ObjectIdField(required=True, allow_none=False)
    selected_option_id = ObjectIdField(required=False, allow_none=True)
    selected_option_ids = ma_fields.List(ObjectIdField(), required=True)
    score = ma_fields.Integer(required=True)
    is_correct = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class CbtSubmissionLog(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(CbtSubmissionLogData)
    collection_name = "cbt_submission_log"
    schema = CbtSubmissionLogSchema
    search = ["score"]
    object_class = CbtSubmissionLogData
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
        "participant": {
            "local": "participant_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.cbt_exam_participant"
            ).cbt_exam_participant.CbtExamParticipant(),
        },
        "exam": {
            "local": "exam_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.cbt_exam").cbt_exam.CbtExam(),
        },
        "question": {
            "local": "question_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.cbt_question"
            ).cbt_question.CbtQuestion(),
        },
        "selected_option": {
            "local": "selected_option_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.cbt_question_option"
            ).cbt_question_option.CbtQuestionOption(),
        },
        "selected_options": {
            "local": "selected_option_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.cbt_question_option"
            ).cbt_question_option.CbtQuestionOption(),
        },
    }
