from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields

from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class MutabaahGroupData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    name: str
    parent_id: Optional[ObjectId] = field(default=None)
    child_ids: Optional[List[ObjectId]] = field(default_factory=list)
    sequence: int
    is_parent: bool
    is_child: bool
    practice_ids: Optional[List[ObjectId]] = field(default_factory=list)
    rubric_id: ObjectId


class MutabaahGroupSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    parent_id = ObjectIdField(required=True, allow_none=True)
    child_ids = ma_fields.List(ObjectIdField(), required=True)
    sequence = ma_fields.Integer(required=True)
    is_parent = ma_fields.Boolean(required=True)
    is_child = ma_fields.Boolean(required=True)
    practice_ids = ma_fields.List(ObjectIdField(), required=True)
    rubric_id = ObjectIdField(required=True, allow_none=True)
    _id = ObjectIdField(required=False, allow_none=True)


class MutabaahGroup(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(MutabaahGroupData)
    collection_name = "mutabaah_group"
    schema = MutabaahGroupSchema
    search = ["name"]
    object_class = MutabaahGroupData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.school_school").school_school.SchoolSchool(),
        },
        "parent": {
            "local": "parent_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_group").mutabaah_group.MutabaahGroup(),
        },
        "children": {
            "local": "child_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_group").mutabaah_group.MutabaahGroup(),
        },
        "practice": {
            "local": "practice_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_practice_type").mutabaah_practice_type.MutabaahPracticeType(),
        },
        "rubric": {
            "local": "rubric_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.mutabaah_practice_rubric").mutabaah_practice_rubric.MutabaahPracticeRubric(),
        },
    }
