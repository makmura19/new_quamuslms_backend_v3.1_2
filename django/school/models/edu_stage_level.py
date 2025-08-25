from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduStageLevelData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    degree_id: Optional[ObjectId] = field(default=None)
    group_id: ObjectId
    name: str
    sequence: int
    is_final: bool
    is_extension: bool
    subject_ids: Optional[List[ObjectId]] = field(default_factory=list)


class EduStageLevelSchema(Schema):
    degree_id = ObjectIdField(required=False, allow_none=True)
    group_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    sequence = ma_fields.Integer(required=True)
    is_final = ma_fields.Boolean(required=True)
    is_extension = ma_fields.Boolean(required=True)
    subject_ids = ma_fields.List(ObjectIdField(), required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class EduStageLevel(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduStageLevelData)
    collection_name = "edu_stage_level"
    schema = EduStageLevelSchema
    search = ["name"]
    object_class = EduStageLevelData
    foreign_key = {
        "degree": {
            "local": "degree_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_degree").edu_degree.EduDegree(),
        },
        "group": {
            "local": "group_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_stage_group"
            ).edu_stage_group.EduStageGroup(),
        },
        "subjects": {
            "local": "subject_ids",
            "foreign": "_id",
            "fields": "_id,name,short_name,sequence",
            "sort": "sequence",
            "model": lambda: __import__("models.edu_subject").edu_subject.EduSubject(),
        },
    }
