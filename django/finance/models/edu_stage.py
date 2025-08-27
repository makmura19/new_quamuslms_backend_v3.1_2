from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduStageData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    group_id: ObjectId
    name: str
    short_name: str
    origin: str
    level_ids: Optional[List[ObjectId]] = field(default_factory=list)


class EduStageSchema(Schema):
    group_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    short_name = ma_fields.String(required=True)
    origin = ma_fields.String(
        validate=validate.OneOf(
            ["domestic", "religion", "vocational", "graduate", "boarding"]
        ),
        required=True,
    )
    level_ids = ma_fields.List(ObjectIdField(), required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class EduStage(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduStageData)
    collection_name = "edu_stage"
    schema = EduStageSchema
    search = ["name", "short_name"]
    object_class = EduStageData
    foreign_key = {
        "group": {
            "local": "group_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_stage_group"
            ).edu_stage_group.EduStageGroup(),
        },
        "level": {
            "local": "level_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_stage_level"
            ).edu_stage_level.EduStageLevel(),
        },
    }
