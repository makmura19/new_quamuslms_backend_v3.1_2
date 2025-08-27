from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceVaVendorData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    bank_id: ObjectId
    code: str
    name: str
    short_name: str
    is_active: bool


class FinanceVaVendorSchema(Schema):
    bank_id = ObjectIdField(required=True, allow_none=False)
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    short_name = ma_fields.String(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceVaVendor(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceVaVendorData)
    collection_name = "finance_va_vendor"
    schema = FinanceVaVendorSchema
    search = ["code", "name", "short_name"]
    object_class = FinanceVaVendorData
    foreign_key = {
        "bank": {
            "local": "bank_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_bank").res_bank.ResBank(),
        }
    }
