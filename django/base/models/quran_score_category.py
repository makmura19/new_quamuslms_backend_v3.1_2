from dataclasses import dataclass, field
from typing import Optional, Union
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranScoreCategoryData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: Optional[ObjectId] = field(default=None)
    type_id: ObjectId
    name: str
    description: str
    penalty_point: Union[int, float]
    max_score: int
    min_score: int


class QuranScoreCategorySchema(Schema):
    school_id = ObjectIdField(required=False, allow_none=True)
    type_id = ObjectIdField(required=True)
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    penalty_point = ma_fields.Float(required=True)
    max_score = ma_fields.Integer(required=True)
    min_score = ma_fields.Integer(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranScoreCategory(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranScoreCategoryData)
    collection_name = "quran_score_category"
    schema = QuranScoreCategorySchema
    search = ["name", "description"]
    object_class = QuranScoreCategoryData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "type": {
            "local": "type_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_score_type"
            ).quran_score_type.QuranScoreType(),
        },
    }
