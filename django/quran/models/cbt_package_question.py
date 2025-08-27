from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class CbtPackageQuestionData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    package_id: ObjectId
    question_id: ObjectId
    custom_score: Optional[int] = field(default=None)
    sequence: int


class CbtPackageQuestionSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    package_id = ObjectIdField(required=True, allow_none=False)
    question_id = ObjectIdField(required=True, allow_none=False)
    custom_score = ma_fields.Integer(required=False, allow_none=True)
    sequence = ma_fields.Integer(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class CbtPackageQuestion(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(CbtPackageQuestionData)
    collection_name = "cbt_package_question"
    schema = CbtPackageQuestionSchema
    search = ["sequence"]
    object_class = CbtPackageQuestionData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "package": {
            "local": "package_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.cbt_package").cbt_package.CbtPackage(),
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
