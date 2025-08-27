from dataclasses import dataclass, field
from typing import Optional, Union
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranTargetScoreMatrixData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    type: str
    level_id: ObjectId
    level_seq: int
    semester_seq: int
    percentage: Union[int, float]
    score: Union[int, float]


class QuranTargetScoreMatrixSchema(Schema):
    school_id = ObjectIdField(required=True)
    type = ma_fields.String(
        validate=validate.OneOf(["regular", "special"]), required=True
    )
    level_id = ObjectIdField(required=True)
    level_seq = ma_fields.Integer(required=True)
    semester_seq = ma_fields.Integer(required=True)
    percentage = ma_fields.Float(required=True)
    score = ma_fields.Float(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranTargetScoreMatrix(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranTargetScoreMatrixData)
    collection_name = "quran_target_score_matrix"
    schema = QuranTargetScoreMatrixSchema
    search = ["type", "level_seq", "semester_seq"]
    object_class = QuranTargetScoreMatrixData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "level": {
            "local": "level_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_stage_level"
            ).edu_stage_level.EduStageLevel(),
        },
    }
