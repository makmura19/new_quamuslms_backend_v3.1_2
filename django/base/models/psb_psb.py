from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class PsbPsbData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    staff_ids: Optional[List[ObjectId]] = field(default_factory=list)
    va_config_id: Optional[ObjectId] = field(default=None)
    name: str
    document_ids: Optional[List[ObjectId]] = field(default_factory=list)
    invoice_ids: Optional[List[ObjectId]] = field(default_factory=list)
    logistic_ids: Optional[List[ObjectId]] = field(default_factory=list)
    fee: int
    is_school: bool
    is_holding: bool
    is_active: bool


class PsbPsbSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    staff_ids = ma_fields.List(ObjectIdField(), required=True)
    va_config_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    document_ids = ma_fields.List(ObjectIdField(), required=True)
    invoice_ids = ma_fields.List(ObjectIdField(), required=True)
    logistic_ids = ma_fields.List(ObjectIdField(), required=True)
    fee = ma_fields.Integer(required=True)
    is_school = ma_fields.Boolean(required=True)
    is_holding = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class PsbPsb(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(PsbPsbData)
    collection_name = "psb_psb"
    schema = PsbPsbSchema
    search = ["name"]
    object_class = PsbPsbData
    foreign_key = {
        "holding": {
            "local": "holding_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, display_name",
            "model": lambda: __import__("models.school_holding").school_holding.SchoolHolding(),
        },
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, code, short_name",
            "model": lambda: __import__("models.school_school").school_school.SchoolSchool(),
        },
        "staff": {
            "local": "staff_ids",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name",
            "model": lambda: __import__("models.school_staff").school_staff.SchoolStaff(),
        },
        "va_config": {
            "local": "va_config_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, prefix, account_no, account_name",
            "model": lambda: __import__("models.finance_va_config").finance_va_config.FinanceVaConfig(),
        },
        "document": {
            "local": "document_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.psb_document").psb_document.PsbDocument(),
        },
        "invoice": {
            "local": "invoice_ids",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, month, semester",
            "model": lambda: __import__("models.psb_invoice").psb_invoice.PsbInvoice(),
        },
        "logistic": {
            "local": "logistic_ids",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, gender, boarding, qty, qty_unit",
            "model": lambda: __import__("models.psb_logistic").psb_logistic.PsbLogistic(),
        },
    }
