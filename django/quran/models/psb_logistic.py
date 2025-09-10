from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class PsbLogisticData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    psb_id: ObjectId
    target_school_ids: Optional[List[ObjectId]] = field(default_factory=list)
    gender: str
    boarding: str
    name: str
    qty: int
    qty_unit: str


class PsbLogisticSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    psb_id = ObjectIdField(required=True, allow_none=False)
    target_school_ids = ma_fields.List(ObjectIdField(), required=True)
    gender = ma_fields.String(validate=validate.OneOf(["male", "female", "all"]), required=True)
    boarding = ma_fields.String(validate=validate.OneOf(["boarding", "no_boarding", "all"]), required=True)
    name = ma_fields.String(required=True)
    qty = ma_fields.Integer(required=True)
    qty_unit = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class PsbLogistic(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(PsbLogisticData)
    collection_name = "psb_logistic"
    schema = PsbLogisticSchema
    search = ["name"]
    object_class = PsbLogisticData
    foreign_key = {
        "holding": {
            "local": "holding_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, display_name",
            "model": lambda: __import__("models.school_holding").school_holding.SchoolHolding(),
        },
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, code, short_name",
            "model": lambda: __import__("models.school_school").school_school.SchoolSchool(),
        },
        "psb": {
            "local": "psb_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name",
            "model": lambda: __import__("models.psb_psb").psb_psb.PsbPsb(),
        },
        "target_schools": {
            "local": "target_school_ids",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, code, short_name",
            "model": lambda: __import__("models.school_school").school_school.SchoolSchool(),
        },
    }
