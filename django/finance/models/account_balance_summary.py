from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class AccountBalanceSummaryData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    coa_id: ObjectId
    code: str
    period: str
    begin_balance: int
    debit: int
    credit: int
    end_balance: int


class AccountBalanceSummarySchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    coa_id = ObjectIdField(required=True, allow_none=False)
    code = ma_fields.String(required=True)
    period = ma_fields.String(required=True)
    begin_balance = ma_fields.Integer(required=True)
    debit = ma_fields.Integer(required=True)
    credit = ma_fields.Integer(required=True)
    end_balance = ma_fields.Integer(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class AccountBalanceSummary(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(AccountBalanceSummaryData)
    collection_name = "account_balance_summary"
    schema = AccountBalanceSummarySchema
    search = ["code", "period"]
    object_class = AccountBalanceSummaryData
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
        "coa": {
            "local": "coa_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
    }
