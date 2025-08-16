from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class ResLocProvinceData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    name: str


class ResLocProvinceSchema(Schema):
    name = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ResLocProvince(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ResLocProvinceData)
    collection_name = "res_loc_province"
    schema = ResLocProvinceSchema
    search = ["name"]
    object_class = ResLocProvinceData
    foreign_key = {}
