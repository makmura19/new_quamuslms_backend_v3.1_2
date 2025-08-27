from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class AccountAccountData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    code: str
    name: str
    type: str
    group: str
    parent_id: Optional[ObjectId] = field(default=None)
    child_ids: Optional[List[ObjectId]] = field(default_factory=list)
    sequence: int
    note: str
    display_name: str
    is_active: Optional[bool] = field(default=True)
    is_manual: Optional[bool] = field(default=True)
    is_group: Optional[bool] = field(default=False)
    is_template: Optional[bool] = field(default=False)
    is_postable: Optional[bool] = field(default=False)


class AccountAccountSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    type = ma_fields.String(
        validate=validate.OneOf(["asset", "liability", "income", "expense", "equity"]),
        required=True,
    )
    group = ma_fields.String(
        validate=validate.OneOf(
            [
                "bank",
                "cash",
                "student_receivable",
                "vendor_payable",
                "merchant_payable",
                "student_saving_payable",
                "parent_refund_payable",
                "tuition_income",
                "donation_income",
                "operational_expense",
                "salary_expense",
                "teaching_material_expense",
                "other",
            ]
        ),
        required=True,
    )
    parent_id = ObjectIdField(required=False, allow_none=True)
    child_ids = ma_fields.List(ObjectIdField(), required=True)
    sequence = ma_fields.Integer(required=True)
    note = ma_fields.String(required=True)
    display_name = ma_fields.String(required=True)
    is_active = ma_fields.Boolean(required=True)
    is_manual = ma_fields.Boolean(required=True)
    is_group = ma_fields.Boolean(required=True)
    is_template = ma_fields.Boolean(required=True)
    is_postable = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class AccountAccount(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(AccountAccountData)
    collection_name = "account_account"
    schema = AccountAccountSchema
    search = ["code", "name", "display_name"]
    object_class = AccountAccountData
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
        "parent": {
            "local": "parent_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
        "child": {
            "local": "child_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
    }
