from dataclasses import dataclass, field
from typing import Optional, List
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
class MutabaahPracticeTypeData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    name: str
    description: Optional[str] = field(default="")
    type: str
    day_count: Optional[int] = field(default=None)
    unit: Optional[str] = field(default=None)
    period: str
    interval: Optional[int] = field(default=None)
    penalty_per_interval: Optional[int] = field(default=None)
    options: Optional[List[OptionItemData]] = field(default_factory=list)
    days_of_week: Optional[List[int]] = field(default_factory=list)
    gender: str
    weight: Optional[int] = field(default=None)
    min_score: Optional[int] = field(default=None)
    max_score: Optional[int] = field(default=None)
    weight_formula: Optional[str] = field(default="weight")
    sequence: int
    mandatory_type: str
    submitted_by: str
    rubric_id: Optional[ObjectId] = field(default=None)
    day_count_ids: Optional[List[ObjectId]] = field(default_factory=list)
    use_timeconfig: Optional[bool] = field(default=False)
    use_penalty: Optional[bool] = field(default=False)
    has_day_count: Optional[bool] = field(default=False)
    is_mandatory_shalat: bool
    is_template: Optional[bool] = field(default=False)


class MutabaahPracticeTypeSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    type = ma_fields.String(
        validate=validate.OneOf(["boolean", "quantitative", "options", "time"]),
        required=True,
    )
    day_count = ma_fields.Integer(required=False, allow_none=True)
    unit = ma_fields.String(required=False, allow_none=True)
    period = ma_fields.String(
        validate=validate.OneOf(["day", "week", "month", "semester", "year"]),
        required=True,
    )
    interval = ma_fields.Integer(required=False, allow_none=True)
    penalty_per_interval = ma_fields.Integer(required=False, allow_none=True)
    options = ma_fields.List(ma_fields.Nested(OptionItemSchema), required=True)
    days_of_week = ma_fields.List(ma_fields.Integer(), required=True)
    gender = ma_fields.String(
        validate=validate.OneOf(["male", "female", "all"]), required=True
    )
    weight = ma_fields.Integer(required=False, allow_none=True)
    min_score = ma_fields.Integer(required=False, allow_none=True)
    max_score = ma_fields.Integer(required=False, allow_none=True)
    weight_formula = ma_fields.String(
        validate=validate.OneOf(["range", "weight"]), required=True
    )
    sequence = ma_fields.Integer(required=True)
    mandatory_type = ma_fields.String(
        validate=validate.OneOf(["wajib", "sunah"]), required=True
    )
    submitted_by = ma_fields.String(
        validate=validate.OneOf(["parent", "teacher", "all"]), required=True
    )
    rubric_id = ObjectIdField(required=True, allow_none=True)
    day_count_ids = ma_fields.List(ObjectIdField(), required=True)
    use_timeconfig = ma_fields.Boolean(required=True)
    use_penalty = ma_fields.Boolean(required=True)
    has_day_count = ma_fields.Boolean(required=True)
    is_mandatory_shalat = ma_fields.Boolean(required=True)
    is_template = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class MutabaahPracticeType(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(MutabaahPracticeTypeData)
    collection_name = "mutabaah_practice_type"
    schema = MutabaahPracticeTypeSchema
    search = ["name", "type", "period"]
    object_class = MutabaahPracticeTypeData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.school_school").school_school.SchoolSchool(),
        },
        "rubric": {
            "local": "rubric_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_practice_rubric").mutabaah_practice_rubric.MutabaahPracticeRubric(),
        },
        "day_count": {
            "local": "day_count_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_practice_type_day").mutabaah_practice_type_day.MutabaahPracticeTypeDay(),
        },
    }
