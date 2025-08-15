from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from datetime import datetime, timezone

from marshmallow import Schema, fields as ma_fields

from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class ResFileData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    company_id: Optional[ObjectId] = field(default=None)
    user_id: Optional[ObjectId] = field(default=None)
    name: str
    url: str
    size_byte: int
    readable_size: str
    upload_date: Optional[datetime] = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ResFileSchema(Schema):
    company_id = ObjectIdField(required=False, allow_none=True)
    user_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    url = ma_fields.String(required=True)
    size_byte = ma_fields.Integer(required=True)
    readable_size = ma_fields.String(required=True)
    upload_date = ma_fields.DateTime(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ResFile(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ResFileData)
    collection_name = "res_file"
    schema = ResFileSchema
    search = ["name", "url"]
    object_class = ResFileData
    foreign_key = {
        "company": {
            "local": "company_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_company").res_company.ResCompany(),
        },
        "user": {
            "local": "user_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_user").res_user.ResUser(),
        },
    }
