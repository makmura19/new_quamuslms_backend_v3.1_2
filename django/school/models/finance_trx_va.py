from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceTrxVaData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    bank_id: ObjectId
    vendor_id: ObjectId
    va_id: ObjectId
    school_id: ObjectId
    student_id: ObjectId
    student_nis: str
    student_name: str
    va_no: str
    trx_id: str
    trx_type: Optional[str] = field(default=None)
    date: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))
    amount: int
    is_execute: bool


class FinanceTrxVaSchema(Schema):
    bank_id = ObjectIdField(required=True, allow_none=False)
    vendor_id = ObjectIdField(required=True, allow_none=False)
    va_id = ObjectIdField(required=True, allow_none=False)
    school_id = ObjectIdField(required=True, allow_none=False)
    student_id = ObjectIdField(required=True, allow_none=False)
    student_nis = ma_fields.String(required=True)
    student_name = ma_fields.String(required=True)
    va_no = ma_fields.String(required=True)
    trx_id = ma_fields.String(required=True)
    trx_type = ma_fields.String(required=False, allow_none=True)
    date = ma_fields.DateTime(required=True)
    amount = ma_fields.Integer(required=True)
    is_execute = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceTrxVa(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceTrxVaData)
    collection_name = "finance_trx_va"
    schema = FinanceTrxVaSchema
    search = ["student_nis", "student_name", "va_no", "trx_id"]
    object_class = FinanceTrxVaData
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
        "va": {
            "local": "va_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.finance_va").finance_va.FinanceVa(),
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
    }
