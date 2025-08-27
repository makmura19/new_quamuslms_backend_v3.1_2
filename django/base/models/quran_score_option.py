from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranScoreOptionData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    category_id: Optional[ObjectId] = field(default=None)
    type_id: ObjectId
    name: str
    score: Optional[int] = field(default=None)
    penalty_point: Optional[int] = field(default=None)
    is_penalty: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=True)
    under_category: Optional[bool] = field(default=False)
    use_parent_score: Optional[bool] = field(default=False)


class QuranScoreOptionSchema(Schema):
    category_id = ObjectIdField(required=False, allow_none=True)
    type_id = ObjectIdField(required=True)
    name = ma_fields.String(required=True)
    score = ma_fields.Integer(required=False, allow_none=True)
    penalty_point = ma_fields.Integer(required=False, allow_none=True)
    is_penalty = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    under_category = ma_fields.Boolean(required=True)
    use_parent_score = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranScoreOption(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranScoreOptionData)
    collection_name = "quran_score_option"
    schema = QuranScoreOptionSchema
    search = ["name"]
    object_class = QuranScoreOptionData
    foreign_key = {
        "category": {
            "local": "category_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_score_category"
            ).quran_score_category.QuranScoreCategory(),
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
