from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime, timezone

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolRepositoryData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    owner_id: Optional[ObjectId] = field(default=None)
    allowed_teacher_ids: Optional[List[ObjectId]] = field(default_factory=list)
    type: str
    file_type: str
    folder_tree: Optional[List[ObjectId]] = field(default_factory=list)
    name: str
    ext: str
    url: Optional[str] = field(default=None)
    size: Optional[int] = field(default=None)
    size_name: Optional[str] = field(default=None)
    date: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))
    is_public: Optional[bool] = field(default=False)
    is_admin: Optional[bool] = field(default=False)
    is_teacher: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=False)


class SchoolRepositorySchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    owner_id = ObjectIdField(required=False, allow_none=True)
    allowed_teacher_ids = ma_fields.List(ObjectIdField(), required=True)
    type = ma_fields.String(validate=validate.OneOf(["file", "folder"]), required=True)
    file_type = ma_fields.String(
        validate=validate.OneOf(
            [
                "other",
                "xls",
                "xlsx",
                "jpg",
                "jpeg",
                "png",
                "doc",
                "docx",
                "ppt",
                "pptx",
                "pdf",
                "mp4",
                "avi",
                "mov",
                "txt",
            ]
        ),
        required=True,
    )
    folder_tree = ma_fields.List(ObjectIdField(), required=True)
    name = ma_fields.String(required=True)
    ext = ma_fields.String(required=True)
    url = ma_fields.String(required=False, allow_none=True)
    size = ma_fields.Integer(required=False, allow_none=True)
    size_name = ma_fields.String(required=False, allow_none=True)
    date = ma_fields.DateTime(required=True)
    is_public = ma_fields.Boolean(required=True)
    is_admin = ma_fields.Boolean(required=True)
    is_teacher = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolRepository(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolRepositoryData)
    collection_name = "school_repository"
    schema = SchoolRepositorySchema
    search = ["name", "file_type"]
    object_class = SchoolRepositoryData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "owner": {
            "local": "owner_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "allowed_teachers": {
            "local": "allowed_teacher_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
    }
