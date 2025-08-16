from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SummaryData:
    parent_balance: int
    pocket_balance: int
    quamus_balance: int
    merchant_balance: int
    unpaid_invoice: int
    male_student_count: int
    female_student_count: int
    male_teacher_count: int
    female_teacher_count: int


@dataclass(kw_only=True)
class SchoolHoldingData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    code: str
    partner_id: ObjectId
    name: str
    display_name: Optional[str] = field(default="")
    logo_sm: Optional[str] = field(default=None)
    logo_md: Optional[str] = field(default=None)
    logo_hd: Optional[str] = field(default=None)
    school_ids: Optional[List[ObjectId]] = field(default_factory=list)
    contact_ids: Optional[List[ObjectId]] = field(default_factory=list)
    staff_ids: Optional[List[ObjectId]] = field(default_factory=list)
    config_finance_id: Optional[ObjectId] = field(default=None)
    config_va_ids: Optional[List[ObjectId]] = field(default_factory=list)
    join_date: Optional[datetime] = field(default=None)
    module_ids: Optional[List[ObjectId]] = field(default_factory=list)
    module_codes: Optional[List[str]] = field(default_factory=list)
    is_account_created: Optional[bool] = field(default=False)
    summary: Optional[SummaryData] = field(
        default_factory=lambda: {
            "parent_balance": 0,
            "pocket_balance": 0,
            "quamus_balance": 0,
            "merchant_balance": 0,
            "unpaid_invoice": 0,
            "male_student_count": 0,
            "female_student_count": 0,
            "male_teacher_count": 0,
            "female_teacher_count": 0,
        }
    )
    payable_id: Optional[ObjectId] = field(default=None)
    cash_id: Optional[ObjectId] = field(default=None)
    dormitory_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_active: bool


class SummarySchema(Schema):
    parent_balance = ma_fields.Integer(required=True)
    pocket_balance = ma_fields.Integer(required=True)
    quamus_balance = ma_fields.Integer(required=True)
    merchant_balance = ma_fields.Integer(required=True)
    unpaid_invoice = ma_fields.Integer(required=True)
    male_student_count = ma_fields.Integer(required=True)
    female_student_count = ma_fields.Integer(required=True)
    male_teacher_count = ma_fields.Integer(required=True)
    female_teacher_count = ma_fields.Integer(required=True)


class SchoolHoldingSchema(Schema):
    code = ma_fields.String(required=True)
    partner_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    display_name = ma_fields.String(required=True)
    logo_sm = ma_fields.String(required=False, allow_none=True)
    logo_md = ma_fields.String(required=False, allow_none=True)
    logo_hd = ma_fields.String(required=False, allow_none=True)
    school_ids = ma_fields.List(ObjectIdField(), required=True)
    contact_ids = ma_fields.List(ObjectIdField(), required=True)
    staff_ids = ma_fields.List(ObjectIdField(), required=True)
    config_finance_id = ObjectIdField(required=False, allow_none=True)
    config_va_ids = ma_fields.List(ObjectIdField(), required=True)
    join_date = ma_fields.DateTime(required=False, allow_none=True)
    module_ids = ma_fields.List(ObjectIdField(), required=True)
    module_codes = ma_fields.List(ma_fields.String(), required=True)
    is_account_created = ma_fields.Boolean(required=True)
    summary = ma_fields.Nested(SummarySchema, required=True)
    payable_id = ObjectIdField(required=False, allow_none=True)
    cash_id = ObjectIdField(required=False, allow_none=True)
    dormitory_ids = ma_fields.List(ObjectIdField(), required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolHolding(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolHoldingData)
    collection_name = "school_holding"
    schema = SchoolHoldingSchema
    search = ["name", "display_name", "module_codes"]
    object_class = SchoolHoldingData
    foreign_key = {
        "partner": {
            "local": "partner_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_partner").res_partner.ResPartner(),
        },
        "schools": {
            "local": "school_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "contacts": {
            "local": "contact_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_partner").res_partner.ResPartner(),
        },
        "staffs": {
            "local": "staff_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_staff"
            ).school_staff.SchoolStaff(),
        },
        "config_finance": {
            "local": "config_finance_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.config_finance"
            ).config_finance.ConfigFinance(),
        },
        "config_vas": {
            "local": "config_va_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.config_va").config_va.ConfigVa(),
        },
        "modules": {
            "local": "module_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_module"
            ).school_module.SchoolModule(),
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
        "dormitories": {
            "local": "dormitory_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_dormitory"
            ).school_dormitory.SchoolDormitory(),
        },
    }
