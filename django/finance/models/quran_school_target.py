from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranSchoolTargetData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    level_id: Optional[ObjectId] = field(default=None)
    level_seq: Optional[int] = field(default=None)
    semester_seq: Optional[int] = field(default=None)
    type: str
    target_type: str
    name: str
    verse_from_seq: int
    verse_to_seq: int
    sequence: int


class QuranSchoolTargetSchema(Schema):
    school_id = ObjectIdField(required=True)
    level_id = ObjectIdField(required=False, allow_none=True)
    level_seq = ma_fields.Integer(required=False, allow_none=True)
    semester_seq = ma_fields.Integer(required=False, allow_none=True)
    type = ma_fields.String(
        validate=validate.OneOf(["regular", "special", "extracurricular"]),
        required=True,
    )
    target_type = ma_fields.String(
        validate=validate.OneOf(["juz", "chapter", "custom"]), required=True
    )
    name = ma_fields.String(required=True)
    verse_from_seq = ma_fields.Integer(required=True)
    verse_to_seq = ma_fields.Integer(required=True)
    sequence = ma_fields.Integer(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranSchoolTarget(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranSchoolTargetData)
    collection_name = "quran_school_target"
    schema = QuranSchoolTargetSchema
    search = ["name", "type", "target_type"]
    object_class = QuranSchoolTargetData
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
