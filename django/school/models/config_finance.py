from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class ReceiptData:
    header: str
    place: str


class ReceiptSchema(Schema):
    header = ma_fields.String(required=True)
    place = ma_fields.String(required=True)


@dataclass(kw_only=True)
class ConfigFinanceData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    payable_id: Optional[ObjectId] = field(default=None)
    cash_id: Optional[ObjectId] = field(default=None)
    sharing_percentage: int
    daily_pocket_treshold: Optional[int] = field(default=None)
    company_fee: int
    prefix: str
    is_auto_debit: bool
    is_pocket_auto_debit: bool
    va_config_ids: Optional[List[ObjectId]] = field(default_factory=list)
    receipt: ReceiptData
    merchant_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_prefix_lock: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=True)


class ConfigFinanceSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    payable_id = ObjectIdField(required=False, allow_none=True)
    cash_id = ObjectIdField(required=False, allow_none=True)
    sharing_percentage = ma_fields.Integer(required=True)
    daily_pocket_treshold = ma_fields.Integer(required=False, allow_none=True)
    company_fee = ma_fields.Integer(required=True)
    prefix = ma_fields.String(required=True)
    is_auto_debit = ma_fields.Boolean(required=True)
    is_pocket_auto_debit = ma_fields.Boolean(required=True)
    va_config_ids = ma_fields.List(ObjectIdField(), required=True)
    receipt = ma_fields.Nested(ReceiptSchema, required=True)
    merchant_ids = ma_fields.List(ObjectIdField(), required=True)
    is_prefix_lock = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ConfigFinance(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ConfigFinanceData)
    collection_name = "config_finance"
    schema = ConfigFinanceSchema
    search = ["prefix"]
    object_class = ConfigFinanceData
    foreign_key = {
        "holding": {
            "local": "holding_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_holding"
            ).school_holding.SchoolHolding(),
        },
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "payable": {
            "local": "payable_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
        "cash": {
            "local": "cash_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
        "va_config": {
            "local": "va_config_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_va_config"
            ).finance_va_config.FinanceVaConfig(),
        },
        "merchant": {
            "local": "merchant_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_merchant"
            ).finance_merchant.FinanceMerchant(),
        },
    }
