from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceTrxParentData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    academic_year_id: ObjectId
    semester_id: ObjectId
    student_id: ObjectId
    student_nis: str
    student_name: str
    invoice_id: Optional[ObjectId] = field(default=None)
    name: str
    debit: int
    credit: int
    final_balance: int
    date: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))


class FinanceTrxParentSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    academic_year_id = ObjectIdField(required=True, allow_none=False)
    semester_id = ObjectIdField(required=True, allow_none=False)
    student_id = ObjectIdField(required=True, allow_none=False)
    student_nis = ma_fields.String(required=True)
    student_name = ma_fields.String(required=True)
    invoice_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    debit = ma_fields.Integer(required=True)
    credit = ma_fields.Integer(required=True)
    final_balance = ma_fields.Integer(required=True)
    date = ma_fields.DateTime(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceTrxParent(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceTrxParentData)
    collection_name = "finance_trx_parent"
    schema = FinanceTrxParentSchema
    search = ["student_nis", "student_name", "name"]
    object_class = FinanceTrxParentData
    foreign_key = {
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
        "semester": {
            "local": "semester_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_semester"
            ).edu_semester.EduSemester(),
        },
        "student": {
            "local": "student_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student"
            ).school_student.SchoolStudent(),
        },
        "invoice": {
            "local": "invoice_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice"
            ).finance_invoice.FinanceInvoice(),
        },
    }
