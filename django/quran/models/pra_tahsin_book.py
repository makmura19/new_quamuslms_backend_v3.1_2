from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields

from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class PraTahsinBookData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: Optional[ObjectId] = field(default=None)
    method_id: ObjectId
    name: str
    level: int
    num_page: int


class PraTahsinBookSchema(Schema):
    school_id = ObjectIdField(required=False, allow_none=True)
    method_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    level = ma_fields.Integer(required=True)
    num_page = ma_fields.Integer(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class PraTahsinBook(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(PraTahsinBookData)
    collection_name = "pra_tahsin_book"
    schema = PraTahsinBookSchema
    search = ["name"]
    object_class = PraTahsinBookData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "method": {
            "local": "method_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.pra_tahsin_method"
            ).pra_tahsin_method.PraTahsinMethod(),
        },
    }