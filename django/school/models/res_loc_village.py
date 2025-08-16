from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class ResLocVillageData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    province_id: ObjectId
    city_id: ObjectId
    district_id: ObjectId
    name: str


class ResLocVillageSchema(Schema):
    province_id = ObjectIdField(required=True, allow_none=False)
    city_id = ObjectIdField(required=True, allow_none=False)
    district_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ResLocVillage(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ResLocVillageData)
    collection_name = "res_loc_village"
    schema = ResLocVillageSchema
    search = ["name"]
    object_class = ResLocVillageData
    foreign_key = {
        "province": {
            "local": "province_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.res_loc_province"
            ).res_loc_province.ResLocProvince(),
        },
        "city": {
            "local": "city_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.res_loc_city"
            ).res_loc_city.ResLocCity(),
        },
        "district": {
            "local": "district_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.res_loc_district"
            ).res_loc_district.ResLocDistrict(),
        },
    }
