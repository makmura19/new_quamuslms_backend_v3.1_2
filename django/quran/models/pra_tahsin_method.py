from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime
from marshmallow import Schema, fields as ma_fields, validate

from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class DeveloperData:
    name: str
    website: str


class DeveloperSchema(Schema):
    name = ma_fields.String(required=True)
    website = ma_fields.String(required=True)


@dataclass(kw_only=True)
class PraTahsinMethodData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: Optional[ObjectId] = field(default=None)
    name: str
    description: str
    image1_url: Optional[str] = field(default=None)
    image2_url: Optional[str] = field(default=None)
    image3_url: Optional[str] = field(default=None)
    type: str
    developer: DeveloperData
    is_developer: bool
    whitelist: Optional[List[ObjectId]] = field(default_factory=list)
    evaluation: str
    preview: bool


class PraTahsinMethodSchema(Schema):
    school_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    image1_url = ma_fields.String(required=False, allow_none=True)
    image2_url = ma_fields.String(required=False, allow_none=True)
    image3_url = ma_fields.String(required=False, allow_none=True)
    type = ma_fields.String(validate=validate.OneOf(["no content", "text", "text image"]), required=True)
    developer = ma_fields.Nested(DeveloperSchema, required=True)
    is_developer = ma_fields.Boolean(required=True)
    whitelist = ma_fields.List(ObjectIdField(), required=True)
    evaluation = ma_fields.String(validate=validate.OneOf(["page", "line"]), required=True)
    preview = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class PraTahsinMethod(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(PraTahsinMethodData)
    collection_name = "pra_tahsin_method"
    schema = PraTahsinMethodSchema
    search = ["name", "description"]
    object_class = PraTahsinMethodData
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
