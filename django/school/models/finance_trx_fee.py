from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceTrxFeeData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    student_id: ObjectId
    student_nis: str
    student_name: str
    debit: int
    credit: int
    final_balance: int
    date: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))


class FinanceTrxFeeSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    student_id = ObjectIdField(required=True, allow_none=False)
    student_nis = ma_fields.String(required=True)
    student_name = ma_fields.String(required=True)
    debit = ma_fields.Integer(required=True)
    credit = ma_fields.Integer(required=True)
    final_balance = ma_fields.Integer(required=True)
    date = ma_fields.DateTime(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceTrxFee(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceTrxFeeData)
    collection_name = "finance_trx_fee"
    schema = FinanceTrxFeeSchema
    search = ["student_nis", "student_name"]
    object_class = FinanceTrxFeeData
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
    }
