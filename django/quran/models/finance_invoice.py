from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceInvoiceData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: ObjectId
    academic_year_id: ObjectId
    semester: Optional[int] = field(default=None)
    year: Optional[int] = field(default=None)
    month: Optional[int] = field(default=None)
    student_id: ObjectId
    student_nis: str
    student_name: str
    type_id: ObjectId
    type: str
    is_installment: bool
    name: str
    amount: int
    paid: int
    rest: int
    status: str
    is_paid_off: Optional[bool] = field(default=False)
    variant_id: Optional[ObjectId] = field(default=None)
    paid_off_at: Optional[datetime] = field(default=None)
    trx_ids: Optional[List[ObjectId]] = field(default_factory=list)


class FinanceInvoiceSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=True, allow_none=False)
    academic_year_id = ObjectIdField(required=True, allow_none=False)
    semester = ma_fields.Integer(required=False, allow_none=True)
    year = ma_fields.Integer(required=False, allow_none=True)
    month = ma_fields.Integer(required=False, allow_none=True)
    student_id = ObjectIdField(required=True, allow_none=False)
    student_nis = ma_fields.String(required=True)
    student_name = ma_fields.String(required=True)
    type_id = ObjectIdField(required=True, allow_none=False)
    type = ma_fields.String(
        validate=validate.OneOf(["month", "semester", "year"]), required=True
    )
    is_installment = ma_fields.Boolean(required=True)
    name = ma_fields.String(required=True)
    amount = ma_fields.Integer(required=True)
    paid = ma_fields.Integer(required=True)
    rest = ma_fields.Integer(required=True)
    status = ma_fields.String(
        validate=validate.OneOf(["waiting_for_payment", "partially_paid", "paid_off"]),
        required=True,
    )
    is_paid_off = ma_fields.Boolean(required=True)
    variant_id = ObjectIdField(required=False, allow_none=True)
    paid_off_at = ma_fields.DateTime(required=False, allow_none=True)
    trx_ids = ma_fields.List(ObjectIdField(), required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceInvoice(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceInvoiceData)
    collection_name = "finance_invoice"
    schema = FinanceInvoiceSchema
    search = ["student_nis", "student_name", "status"]
    object_class = FinanceInvoiceData
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
        "academic_year": {
            "local": "academic_year_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_academic_year"
            ).edu_academic_year.EduAcademicYear(),
        },
        "student": {
            "local": "student_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student"
            ).school_student.SchoolStudent(),
        },
        "type": {
            "local": "type_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice_type"
            ).finance_invoice_type.FinanceInvoiceType(),
        },
        "variant": {
            "local": "variant_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice_price_variant"
            ).finance_invoice_price_variant.FinanceInvoicePriceVariant(),
        },
        "transactions": {
            "local": "trx_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_trx_invoice"
            ).finance_trx_invoice.FinanceTrxInvoice(),
        },
    }
