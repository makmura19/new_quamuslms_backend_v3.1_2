from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceMerchantData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    login: Optional[str] = field(default=None)
    user_id: Optional[ObjectId] = field(default=None)
    name: str
    phone: str
    balance: Optional[int] = field(default=0)
    coa_id: Optional[ObjectId] = field(default=None)
    is_school: Optional[bool] = field(default=False)
    is_holding: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=True)


class FinanceMerchantSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    login = ma_fields.String(required=False, allow_none=True)
    user_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    phone = ma_fields.String(required=True)
    balance = ma_fields.Integer(required=True)
    coa_id = ObjectIdField(required=False, allow_none=True)
    is_school = ma_fields.Boolean(required=True)
    is_holding = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceMerchant(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceMerchantData)
    collection_name = "finance_merchant"
    schema = FinanceMerchantSchema
    search = ["name", "phone"]
    object_class = FinanceMerchantData
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
        "user": {
            "local": "user_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_user").res_user.ResUser(),
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
