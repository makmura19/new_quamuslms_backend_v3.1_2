from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceInvoicePriceData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    type_id: ObjectId
    level_id: ObjectId
    amount: int
    variant_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_active: bool


class FinanceInvoicePriceSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    type_id = ObjectIdField(required=True, allow_none=False)
    level_id = ObjectIdField(required=True, allow_none=False)
    amount = ma_fields.Integer(required=True)
    variant_ids = ma_fields.List(ObjectIdField(), required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceInvoicePrice(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceInvoicePriceData)
    collection_name = "finance_invoice_price"
    schema = FinanceInvoicePriceSchema
    search = ["amount"]
    object_class = FinanceInvoicePriceData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "type": {
            "local": "type_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice_type"
            ).finance_invoice_type.FinanceInvoiceType(),
        },
        "level": {
            "local": "level_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_stage_level"
            ).edu_stage_level.EduStageLevel(),
        },
        "variants": {
            "local": "variant_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice_price_variant"
            ).finance_invoice_price_variant.FinanceInvoicePriceVariant(),
        },
    }
