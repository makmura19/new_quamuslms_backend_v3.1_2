from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranTargetGroupData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    program_type: str
    name: str
    is_active: Optional[bool] = field(default=True)
    target_ids: Optional[List[ObjectId]] = field(default_factory=list)


class QuranTargetGroupSchema(Schema):
    school_id = ObjectIdField(required=True)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    name = ma_fields.String(required=True)
    is_active = ma_fields.Boolean(required=True)
    target_ids = ma_fields.List(ObjectIdField(), required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranTargetGroup(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranTargetGroupData)
    collection_name = "quran_target_group"
    schema = QuranTargetGroupSchema
    search = ["name", "program_type"]
    object_class = QuranTargetGroupData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        }
    }
