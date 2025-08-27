from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceReceiptDetail:
    description: str
    amount: Optional[int] = field(default=None)
    payment: int


@dataclass(kw_only=True)
class FinanceReceiptPrintData:
    cashier: str
    company_name: str
    header: str
    logo: str
    place: str
    name: str
    nis: str
    class_name: str
    school_name: str
    academic_year: str
    method: str
    date: str


@dataclass(kw_only=True)
class FinanceReceiptData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: ObjectId
    student_id: ObjectId
    student_name: str
    student_nis: str
    student_va: Optional[str] = field(default=None)
    receipt_no: str
    date: datetime
    detail: Optional[List[FinanceReceiptDetail]] = field(default_factory=list)
    total: int
    url: Optional[str] = field(default=None)
    method: str
    print_data: FinanceReceiptPrintData
    invoice_ids: Optional[List[ObjectId]] = field(default_factory=list)


class FinanceReceiptDetailSchema(Schema):
    description = ma_fields.String(required=True)
    amount = ma_fields.Integer(required=False, allow_none=True)
    payment = ma_fields.Integer(required=True)


class FinanceReceiptPrintDataSchema(Schema):
    cashier = ma_fields.String(required=True)
    company_name = ma_fields.String(required=True)
    header = ma_fields.String(required=True)
    logo = ma_fields.String(required=True)
    place = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    nis = ma_fields.String(required=True)
    class_name = ma_fields.String(required=True)
    school_name = ma_fields.String(required=True)
    academic_year = ma_fields.String(required=True)
    method = ma_fields.String(required=True)
    date = ma_fields.String(required=True)


class FinanceReceiptSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=True, allow_none=False)
    student_id = ObjectIdField(required=True, allow_none=False)
    student_name = ma_fields.String(required=True)
    student_nis = ma_fields.String(required=True)
    student_va = ma_fields.String(required=False, allow_none=True)
    receipt_no = ma_fields.String(required=True)
    date = ma_fields.DateTime(required=True)
    detail = ma_fields.List(ma_fields.Nested(FinanceReceiptDetailSchema), required=True)
    total = ma_fields.Integer(required=True)
    url = ma_fields.String(required=False, allow_none=True)
    method = ma_fields.String(
        validate=validate.OneOf(["cash", "virtual_account", "parent_balance"]),
        required=True,
    )
    print_data = ma_fields.Nested(FinanceReceiptPrintDataSchema, required=True)
    invoice_ids = ma_fields.List(ObjectIdField(), required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceReceipt(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceReceiptData)
    collection_name = "finance_receipt"
    schema = FinanceReceiptSchema
    search = ["student_nis", "student_name", "receipt_no"]
    object_class = FinanceReceiptData
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
        "student": {
            "local": "student_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student"
            ).school_student.SchoolStudent(),
        },
        "invoices": {
            "local": "invoice_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice"
            ).finance_invoice.FinanceInvoice(),
        },
    }
