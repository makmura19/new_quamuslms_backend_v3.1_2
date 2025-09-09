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
class MutabaahPracticeRuleData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    level_id: ObjectId
    practice_type_id: ObjectId
    type: str
    options: Optional[List[OptionItemData]] = field(default_factory=list)
    days_of_week: Optional[List[int]] = field(default_factory=list)
    period: str
    target: Union[str, bool, int]
    unit: Optional[str] = field(default=None)
    interval: Optional[int] = field(default=None)
    penalty_per_interval: Optional[int] = field(default=None)
    weight: Optional[int] = field(default=None)
    min_score: int
    max_score: int
    submitted_by: str
    use_timeconfig: bool
    use_penalty: bool
    variant_ids: Optional[List[ObjectId]] = field(default_factory=list)
    rubric_id: Optional[ObjectId] = field(default=None)
    is_active: bool


class MutabaahPracticeRuleSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    level_id = ObjectIdField(required=True, allow_none=False)
    practice_type_id = ObjectIdField(required=True, allow_none=False)
    type = ma_fields.String(
        validate=validate.OneOf(["boolean", "quantitative", "options", "time"]),
        required=True,
    )
    options = ma_fields.List(ma_fields.Nested(OptionItemSchema), required=True)
    days_of_week = ma_fields.List(ma_fields.Integer(), required=True)
    period = ma_fields.String(
        validate=validate.OneOf(["day", "week", "month", "semester", "year"]),
        required=True,
    )
    target = ma_fields.Raw(required=True)
    unit = ma_fields.String(required=False, allow_none=True)
    interval = ma_fields.Integer(required=False, allow_none=True)
    penalty_per_interval = ma_fields.Integer(required=False, allow_none=True)
    weight = ma_fields.Integer(required=False, allow_none=True)
    min_score = ma_fields.Integer(required=True)
    max_score = ma_fields.Integer(required=True)
    submitted_by = ma_fields.String(
        validate=validate.OneOf(["parent", "teacher", "all"]), required=True
    )
    use_timeconfig = ma_fields.Boolean(required=True)
    use_penalty = ma_fields.Boolean(required=True)
    variant_ids = ma_fields.List(ObjectIdField(), required=True)
    rubric_id = ObjectIdField(required=True, allow_none=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class MutabaahPracticeRule(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(MutabaahPracticeRuleData)
    collection_name = "mutabaah_practice_rule"
    schema = MutabaahPracticeRuleSchema
    search = ["type", "period"]
    object_class = MutabaahPracticeRuleData
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
        "practice_type": {
            "local": "practice_type_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_practice_type").mutabaah_practice_type.MutabaahPracticeType(),
        },
        "variant": {
            "local": "variant_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_practice_variant").mutabaah_practice_variant.MutabaahPracticeVariant(),
        },
        "rubric": {
            "local": "rubric_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_practice_rubric").mutabaah_practice_rubric.MutabaahPracticeRubric(),
        },
    }
