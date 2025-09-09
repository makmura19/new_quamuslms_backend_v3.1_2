from dataclasses import dataclass, field
from typing import Optional, List, Union
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate

from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class OptionItemData:
    item: str
    score: int


class OptionItemSchema(Schema):
    item = ma_fields.String(required=True)
    score = ma_fields.Integer(required=True)


@dataclass(kw_only=True)
class MutabaahPracticeVariantData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    practice_id: ObjectId
    rule_id: ObjectId
    level_id: Optional[ObjectId] = field(default=None)
    gender: Optional[str] = field(default=None)
    is_boarding: bool
    type: str
    unit: Optional[str] = field(default=None)
    target: Union[str, bool, int]
    options: Optional[List[OptionItemData]] = field(default_factory=list)
    days_of_week: Optional[List[int]] = field(default_factory=list)
    period: str
    interval: Optional[int] = field(default=None)
    penalty_per_interval: Optional[int] = field(default=None)
    weight: Optional[int] = field(default=None)
    min_score: int
    max_score: int
    submitted_by: str
    rubric_id: Optional[ObjectId] = field(default=None)
    use_timeconfig: bool
    use_penalty: bool


class MutabaahPracticeVariantSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    practice_id = ObjectIdField(required=True, allow_none=False)
    rule_id = ObjectIdField(required=True, allow_none=False)
    level_id = ObjectIdField(required=False, allow_none=True)
    gender = ma_fields.String(required=False, allow_none=True)
    is_boarding = ma_fields.Boolean(required=True)
    type = ma_fields.String(
        validate=validate.OneOf(["boolean", "quantitative", "options", "time"]),
        required=True,
    )
    unit = ma_fields.String(required=False, allow_none=True)
    target = ma_fields.Raw(required=True)
    options = ma_fields.List(ma_fields.Nested(OptionItemSchema), required=True)
    days_of_week = ma_fields.List(ma_fields.Integer(), required=True)
    period = ma_fields.String(
        validate=validate.OneOf(["day", "week", "month", "semester", "year"]),
        required=True,
    )
    interval = ma_fields.Integer(required=False, allow_none=True)
    penalty_per_interval = ma_fields.Integer(required=False, allow_none=True)
    weight = ma_fields.Integer(required=False, allow_none=True)
    min_score = ma_fields.Integer(required=True)
    max_score = ma_fields.Integer(required=True)
    submitted_by = ma_fields.String(
        validate=validate.OneOf(["parent", "teacher", "all"]), required=True
    )
    rubric_id = ObjectIdField(required=True, allow_none=True)
    use_timeconfig = ma_fields.Boolean(required=True)
    use_penalty = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class MutabaahPracticeVariant(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(MutabaahPracticeVariantData)
    collection_name = "mutabaah_practice_variant"
    schema = MutabaahPracticeVariantSchema
    search = ["type", "period", "submitted_by"]
    object_class = MutabaahPracticeVariantData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.school_school").school_school.SchoolSchool(),
        },
        "practice": {
            "local": "practice_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_practice_type").mutabaah_practice_type.MutabaahPracticeType(),
        },
        "rule": {
            "local": "rule_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_practice_rule").mutabaah_practice_rule.MutabaahPracticeRule(),
        },
        "level": {
            "local": "level_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_stage_level").edu_stage_level.EduStageLevel(),
        },
        "rubric": {
            "local": "rubric_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_practice_rubric").mutabaah_practice_rubric.MutabaahPracticeRubric(),
        },
    }
