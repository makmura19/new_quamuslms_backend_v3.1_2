from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolStaffData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    partner_id: ObjectId
    payable_id: Optional[ObjectId] = field(default=None)
    cash_id: Optional[ObjectId] = field(default=None)
    balance: Optional[int] = field(default=0)
    name: str
    role_id: Optional[ObjectId] = field(default=None)
    login: Optional[str] = field(default=None)
    user_id: Optional[ObjectId] = field(default=None)


class SchoolStaffSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    partner_id = ObjectIdField(required=True, allow_none=False)
    payable_id = ObjectIdField(required=True, allow_none=False)
    cash_id = ObjectIdField(required=True, allow_none=False)
    balance = ma_fields.Integer(required=True)
    name = ma_fields.String(required=True)
    role_id = ObjectIdField(required=False, allow_none=True)
    login = ma_fields.String(required=False, allow_none=True)
    user_id = ObjectIdField(required=False, allow_none=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolStaff(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolStaffData)
    collection_name = "school_staff"
    schema = SchoolStaffSchema
    search = ["name", "login"]
    object_class = SchoolStaffData
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
        "partner": {
            "local": "partner_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_partner").res_partner.ResPartner(),
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
        "role": {
            "local": "role_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.res_authority"
            ).res_authority.ResAuthority(),
        },
        "user": {
            "local": "user_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_user").res_user.ResUser(),
        },
    }
