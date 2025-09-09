from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduChapterData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    level_id: ObjectId
    subject_id: ObjectId
    name: str
    image: Optional[str] = field(default=None)
    parent_id: Optional[ObjectId] = field(default=None)
    child_ids: Optional[List[ObjectId]] = field(default_factory=list)
    sequence: int
    media_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_active: bool


class EduChapterSchema(Schema):
    level_id = ObjectIdField(required=True, allow_none=False)
    subject_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    image = ma_fields.String(required=False, allow_none=True)
    parent_id = ObjectIdField(required=False, allow_none=True)
    child_ids = ma_fields.List(ObjectIdField(), required=True)
    sequence = ma_fields.Integer(required=True)
    media_ids = ma_fields.List(ObjectIdField(), required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class EduChapter(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduChapterData)
    collection_name = "edu_chapter"
    schema = EduChapterSchema
    search = ["name"]
    object_class = EduChapterData
    foreign_key = {
        "level": {
            "local": "level_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_stage_level").edu_stage_level.EduStageLevel(),
        },
        "subject": {
            "local": "subject_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_subject").edu_subject.EduSubject(),
        },
        "parent": {
            "local": "parent_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_chapter").edu_chapter.EduChapter(),
        },
        "childs": {
            "local": "child_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_chapter").edu_chapter.EduChapter(),
        },
        "medias": {
            "local": "media_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_media").edu_media.EduMedia(),
        },
    }
