from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceVaConfigData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    bank_id: ObjectId
    vendor_id: ObjectId
    coa_id: ObjectId
    holding_id: Optional[ObjectId] = field(default=None)
    school_ids: List[ObjectId]
    prefix: str
    name: str
    account_no: str
    account_name: str
    purpose: str
    fee: int
    partner_id: str
    client_id: str
    client_secret: str
    key: str
    is_active: Optional[bool] = field(default=True)


class FinanceVaConfigSchema(Schema):
    bank_id = ObjectIdField(required=True)
    vendor_id = ObjectIdField(required=True)
    coa_id = ObjectIdField(required=True)
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_ids = ma_fields.List(ObjectIdField(), required=True)
    prefix = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    account_no = ma_fields.String(required=True)
    account_name = ma_fields.String(required=True)
    purpose = ma_fields.String(
        validate=validate.OneOf(["bill", "canteen"]), required=True
    )
    fee = ma_fields.Integer(required=True)
    partner_id = ma_fields.String(required=True)
    client_id = ma_fields.String(required=True)
    client_secret = ma_fields.String(required=True)
    key = ma_fields.String(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceVaConfig(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceVaConfigData)
    collection_name = "finance_va_config"
    schema = FinanceVaConfigSchema
    search = ["prefix", "name", "account_no", "account_name", "purpose"]
    object_class = FinanceVaConfigData
    foreign_key = {
        "bank": {
            "local": "bank_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_bank").res_bank.ResBank(),
        },
        "vendor": {
            "local": "vendor_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_va_vendor"
            ).finance_va_vendor.FinanceVaVendor(),
        },
        "coa": {
            "local": "coa_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
        "holding": {
            "local": "holding_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_holding"
            ).school_holding.SchoolHolding(),
        },
        "schools": {
            "local": "school_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
    }
