from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class CbtQuestionOptionData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    question_id: ObjectId
    text: str
    is_correct: Optional[bool] = field(default=False)


class CbtQuestionOptionSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    question_id = ObjectIdField(required=True, allow_none=False)
    text = ma_fields.String(required=True)
    is_correct = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class CbtQuestionOption(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(CbtQuestionOptionData)
    collection_name = "cbt_question_option"
    schema = CbtQuestionOptionSchema
    search = ["text"]
    object_class = CbtQuestionOptionData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "question": {
            "local": "question_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.cbt_question"
            ).cbt_question.CbtQuestion(),
        },
    }
