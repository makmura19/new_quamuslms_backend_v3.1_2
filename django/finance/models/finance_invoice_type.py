from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceInvoiceTypeData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    type: str
    name: str
    description: str
    due_days: Optional[int] = field(default=None)
    income_coa_id: Optional[ObjectId] = field(default=None)
    payable_coa_id: Optional[ObjectId] = field(default=None)
    is_male: bool
    is_female: bool
    is_installment: bool
    price_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_active: bool


class FinanceInvoiceTypeSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    type = ma_fields.String(
        validate=validate.OneOf(["month", "semester", "year"]), required=True
    )
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    due_days = ma_fields.Integer(required=False, allow_none=True)
    income_coa_id = ObjectIdField(required=False, allow_none=True)
    payable_coa_id = ObjectIdField(required=False, allow_none=True)
    is_male = ma_fields.Boolean(required=True)
    is_female = ma_fields.Boolean(required=True)
    is_installment = ma_fields.Boolean(required=True)
    price_ids = ma_fields.List(ObjectIdField(), required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceInvoiceType(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceInvoiceTypeData)
    collection_name = "finance_invoice_type"
    schema = FinanceInvoiceTypeSchema
    search = ["name", "type"]
    object_class = FinanceInvoiceTypeData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "income_coa": {
            "local": "income_coa_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
        "payable_coa": {
            "local": "payable_coa_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
        "prices": {
            "local": "price_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice_price"
            ).finance_invoice_price.FinanceInvoicePrice(),
        },
    }
