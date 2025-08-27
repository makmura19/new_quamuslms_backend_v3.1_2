from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class ResAuthorityData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    code: str
    name: str
    is_staff: Optional[bool] = field(default=False)
    is_school: Optional[bool] = field(default=False)
    is_holding: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=True)


class ResAuthoritySchema(Schema):
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    is_staff = ma_fields.Boolean(required=True)
    is_school = ma_fields.Boolean(required=True)
    is_holding = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ResAuthority(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ResAuthorityData)
    collection_name = "res_authority"
    schema = ResAuthoritySchema
    search = ["code", "name"]
    object_class = ResAuthorityData
    foreign_key = {}
