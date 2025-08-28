from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields
from marshmallow import validate

from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduSubjectLevelData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    subject_id: ObjectId
    level_id: ObjectId
    name: str
    bar_img: Optional[str] = field(default=None)
    thumbnail_img: Optional[str] = field(default=None)
    subject_seq: int
    is_catalogue: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=True)


class EduSubjectLevelSchema(Schema):
    subject_id = ObjectIdField(required=True, allow_none=False)
    level_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    bar_img = ma_fields.String(required=False, allow_none=True)
    thumbnail_img = ma_fields.String(required=False, allow_none=True)
    subject_seq = ma_fields.Integer(required=True)
    is_catalogue = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class EduSubjectLevel(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduSubjectLevelData)
    collection_name = "edu_subject_level"
    schema = EduSubjectLevelSchema
    search = ["name"]
    object_class = EduSubjectLevelData
    foreign_key = {
        "subject": {
            "local": "subject_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_subject").edu_subject.EduSubject(),
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
