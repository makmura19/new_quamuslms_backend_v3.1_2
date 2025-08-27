from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceVaData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    academic_year_id: ObjectId
    bank_id: ObjectId
    vendor_id: ObjectId
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: ObjectId
    va_config_id: ObjectId
    va_no: str
    is_active: Optional[bool] = field(default=True)


class FinanceVaSchema(Schema):
    academic_year_id = ObjectIdField(required=True, allow_none=False)
    bank_id = ObjectIdField(required=True, allow_none=False)
    vendor_id = ObjectIdField(required=True, allow_none=False)
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=True, allow_none=False)
    va_config_id = ObjectIdField(required=True, allow_none=False)
    va_no = ma_fields.String(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceVa(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceVaData)
    collection_name = "finance_va"
    schema = FinanceVaSchema
    search = ["va_no"]
    object_class = FinanceVaData
    foreign_key = {
        "academic_year": {
            "local": "academic_year_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_academic_year"
            ).edu_academic_year.EduAcademicYear(),
        },
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
        "va_config": {
            "local": "va_config_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_va_config"
            ).finance_va_config.FinanceVaConfig(),
        },
    }
