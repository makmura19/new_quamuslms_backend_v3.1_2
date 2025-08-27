from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceTrxInvoiceData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    invoice_id: ObjectId
    academic_year_id: ObjectId
    semester_id: ObjectId
    type_id: ObjectId
    student_id: ObjectId
    student_name: str
    student_nis: str
    name: str
    amount: int
    method: str
    receipt_id: Optional[ObjectId] = field(default=None)
    move_id: Optional[ObjectId] = field(default=None)
    date: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))


class FinanceTrxInvoiceSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    invoice_id = ObjectIdField(required=True, allow_none=False)
    academic_year_id = ObjectIdField(required=True, allow_none=False)
    semester_id = ObjectIdField(required=True, allow_none=False)
    type_id = ObjectIdField(required=True, allow_none=False)
    student_id = ObjectIdField(required=True, allow_none=False)
    student_name = ma_fields.String(required=True)
    student_nis = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    amount = ma_fields.Integer(required=True)
    method = ma_fields.String(
        validate=validate.OneOf(
            [
                "virtual_account",
                "manual_transfer",
                "cash",
                "ewallet",
                "pocket",
                "parent_balance",
            ]
        ),
        required=True,
    )
    receipt_id = ObjectIdField(required=False, allow_none=True)
    move_id = ObjectIdField(required=False, allow_none=True)
    date = ma_fields.DateTime(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceTrxInvoice(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceTrxInvoiceData)
    collection_name = "finance_trx_invoice"
    schema = FinanceTrxInvoiceSchema
    search = ["student_nis", "student_name", "name", "method"]
    object_class = FinanceTrxInvoiceData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "invoice": {
            "local": "invoice_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice"
            ).finance_invoice.FinanceInvoice(),
        },
        "academic_year": {
            "local": "academic_year_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_academic_year"
            ).edu_academic_year.EduAcademicYear(),
        },
        "semester": {
            "local": "semester_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_semester"
            ).edu_semester.EduSemester(),
        },
        "type": {
            "local": "type_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice_type"
            ).finance_invoice_type.FinanceInvoiceType(),
        },
        "student": {
            "local": "student_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student"
            ).school_student.SchoolStudent(),
        },
        "receipt": {
            "local": "receipt_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_receipt"
            ).finance_receipt.FinanceReceipt(),
        },
        "move": {
            "local": "move_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_move"
            ).account_move.AccountMove(),
        },
    }
