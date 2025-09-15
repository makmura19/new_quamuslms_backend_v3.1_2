from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields

from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class RubricItemData:
    gte: int
    lte: int
    score: int
    description: str


class RubricItemSchema(Schema):
    gte = ma_fields.Integer(required=True)
    lte = ma_fields.Integer(required=True)
    score = ma_fields.Integer(required=True)
    description = ma_fields.String(required=True)


@dataclass(kw_only=True)
class MutabaahPracticeRubricData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    level_id: Optional[ObjectId] = field(default=None)
    name: str
    list: Optional[List[RubricItemData]] = field(default_factory=list)
    is_practice: bool
    is_report: bool
    is_group: bool
    is_program: bool
    is_active: bool


class MutabaahPracticeRubricSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    level_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    list = ma_fields.List(ma_fields.Nested(RubricItemSchema), required=True)
    is_practice = ma_fields.Boolean(required=True)
    is_report = ma_fields.Boolean(required=True)
    is_group = ma_fields.Boolean(required=True)
    is_program = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class MutabaahPracticeRubric(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(MutabaahPracticeRubricData)
    collection_name = "mutabaah_practice_rubric"
    schema = MutabaahPracticeRubricSchema
    search = ["name"]
    object_class = MutabaahPracticeRubricData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.school_school").school_school.SchoolSchool(),
        },
        "level": {
            "local": "level_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_stage_level").edu_stage_level.EduStageLevel(),
        },
    }
