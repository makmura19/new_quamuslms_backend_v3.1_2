from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranScoreTypeData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: Optional[ObjectId] = field(default=None)
    name: str
    program_type: str
    type: Optional[str] = field(default=None)
    rule: Optional[str] = field(default=None)
    min_score: Optional[int] = field(default=None)
    max_score: Optional[int] = field(default=None)
    is_daily: bool
    is_exam: bool
    is_juziyah: bool
    is_fluency: Optional[bool] = field(default=False)
    is_tajweed: Optional[bool] = field(default=False)
    is_report: bool
    has_category: Optional[bool] = field(default=False)
    category_ids: Optional[List[ObjectId]] = field(default_factory=list)
    option_ids: Optional[List[ObjectId]] = field(default_factory=list)
    total_rule: Optional[str] = field(default=None)
    penalty_point: Optional[int] = field(default=None)


class QuranScoreTypeSchema(Schema):
    school_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    type = ma_fields.String(
        validate=validate.OneOf([None, "numeric", "choice", "multi_choice"]),
        allow_none=True,
        required=False,
    )
    rule = ma_fields.String(
        validate=validate.OneOf([None, "accumulative", "average"]),
        allow_none=True,
        required=False,
    )
    min_score = ma_fields.Integer(required=False, allow_none=True)
    max_score = ma_fields.Integer(required=False, allow_none=True)
    is_daily = ma_fields.Boolean(required=True)
    is_exam = ma_fields.Boolean(required=True)
    is_juziyah = ma_fields.Boolean(required=True)
    is_fluency = ma_fields.Boolean(required=True)
    is_tajweed = ma_fields.Boolean(required=True)
    is_report = ma_fields.Boolean(required=True)
    has_category = ma_fields.Boolean(required=True)
    category_ids = ma_fields.List(ObjectIdField(), required=True)
    option_ids = ma_fields.List(ObjectIdField(), required=True)
    total_rule = ma_fields.String(
        validate=validate.OneOf([None, "accumulative", "average"]),
        allow_none=True,
        required=False,
    )
    penalty_point = ma_fields.Integer(required=False, allow_none=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranScoreType(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranScoreTypeData)
    collection_name = "quran_score_type"
    schema = QuranScoreTypeSchema
    search = ["name", "program_type", "type"]
    object_class = QuranScoreTypeData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "categories": {
            "local": "category_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_score_category"
            ).quran_score_category.QuranScoreCategory(),
        },
        "options": {
            "local": "option_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_score_option"
            ).quran_score_option.QuranScoreOption(),
        },
    }
