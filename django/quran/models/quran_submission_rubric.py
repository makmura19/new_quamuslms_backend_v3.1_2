from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranSubmissionRubricData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    program_type: str
    name: str
    gte: int
    lte: int


class QuranSubmissionRubricSchema(Schema):
    school_id = ObjectIdField(required=True)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    name = ma_fields.String(required=True)
    gte = ma_fields.Integer(required=True)
    lte = ma_fields.Integer(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranSubmissionRubric(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranSubmissionRubricData)
    collection_name = "quran_submission_rubric"
    schema = QuranSubmissionRubricSchema
    search = ["name", "program_type"]
    object_class = QuranSubmissionRubricData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, code, name, display_name",
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        }
    }
