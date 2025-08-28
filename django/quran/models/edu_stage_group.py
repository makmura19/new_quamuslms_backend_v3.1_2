from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduStageGroupData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    name: str
    description: str
    sequence: int
    has_degree: bool
    has_faculty: bool
    has_subject_mapping: bool
    has_major: bool
    has_program_type: bool
    duration_years: int
    student_label: str
    has_level: bool
    level_ids: Optional[List[ObjectId]] = field(default_factory=list)
    stage_ids: Optional[List[ObjectId]] = field(default_factory=list)


class EduStageGroupSchema(Schema):
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    sequence = ma_fields.Integer(required=True)
    has_degree = ma_fields.Boolean(required=True)
    has_faculty = ma_fields.Boolean(required=True)
    has_subject_mapping = ma_fields.Boolean(required=True)
    has_major = ma_fields.Boolean(required=True)
    has_program_type = ma_fields.Boolean(required=True)
    duration_years = ma_fields.Integer(required=True)
    student_label = ma_fields.String(required=True)
    has_level = ma_fields.Boolean(required=True)
    level_ids = ma_fields.List(ObjectIdField(), required=True)
    stage_ids = ma_fields.List(ObjectIdField(), required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class EduStageGroup(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduStageGroupData)
    collection_name = "edu_stage_group"
    schema = EduStageGroupSchema
    search = ["name", "description", "student_label"]
    object_class = EduStageGroupData
    foreign_key = {
        "level": {
            "local": "level_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_stage_level"
            ).edu_stage_level.EduStageLevel(),
        },
        "stage": {
            "local": "stage_ids",
            "foreign": "_id",
            "fields": "_id,name,short_name",
            "sort": None,
            "model": lambda: __import__("models.edu_stage").edu_stage.EduStage(),
        },
    }
