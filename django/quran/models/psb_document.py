from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from marshmallow import validate

from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class PsbDocumentData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    psb_id: ObjectId
    school_ids: Optional[List[ObjectId]] = field(default_factory=list)
    name: str
    qty: int
    is_active: bool


class PsbDocumentSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    psb_id = ObjectIdField(required=True, allow_none=False)
    school_ids = ma_fields.List(ObjectIdField(), required=True)
    name = ma_fields.String(required=True)
    qty = ma_fields.Integer(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class PsbDocument(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(PsbDocumentData)
    collection_name = "psb_document"
    schema = PsbDocumentSchema
    search = ["name"]
    object_class = PsbDocumentData
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
        "schools": {
            "local": "school_ids",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, code, short_name",
            "model": lambda: __import__("models.school_school").school_school.SchoolSchool(),
        },
    }
