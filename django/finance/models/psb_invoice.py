from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields

from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class PsbInvoiceData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    invoice_type_id: ObjectId
    month: Optional[List[int]] = field(default_factory=list)
    semester: Optional[List[int]] = field(default_factory=list)
    psb_id: ObjectId


class PsbInvoiceSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    invoice_type_id = ObjectIdField(required=True, allow_none=False)
    month = ma_fields.List(ma_fields.Integer(), required=True)
    semester = ma_fields.List(ma_fields.Integer(), required=True)
    psb_id = ObjectIdField(required=True, allow_none=False)
    _id = ObjectIdField(required=False, allow_none=True)


class PsbInvoice(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(PsbInvoiceData)
    collection_name = "psb_invoice"
    schema = PsbInvoiceSchema
    search = ["invoice_type_id"]
    object_class = PsbInvoiceData
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
        "invoice_type": {
            "local": "invoice_type_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name, type",
            "model": lambda: __import__("models.finance_invoice_type").finance_invoice_type.FinanceInvoiceType(),
        },
        "psb": {
            "local": "psb_id",
            "foreign": "_id",
            "sort": None,
            "fields": "_id, name",
            "model": lambda: __import__("models.psb_psb").psb_psb.PsbPsb(),
        },
    }
