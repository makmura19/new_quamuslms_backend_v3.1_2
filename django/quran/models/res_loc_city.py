from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class ResLocCityData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    province_id: ObjectId
    name: str


class ResLocCitySchema(Schema):
    province_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ResLocCity(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ResLocCityData)
    collection_name = "res_loc_city"
    schema = ResLocCitySchema
    search = ["name"]
    object_class = ResLocCityData
    foreign_key = {
        "province": {
            "local": "province_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.res_loc_province"
            ).res_loc_province.ResLocProvince(),
        }
    }
