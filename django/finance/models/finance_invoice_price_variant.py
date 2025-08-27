from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceInvoicePriceVariantData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    price_id: ObjectId
    type_id: ObjectId
    gender: Optional[str] = field(default=None)
    is_boarding: Optional[bool] = field(default=None)
    is_alumni: Optional[bool] = field(default=None)
    degree_id: Optional[ObjectId] = field(default=None)
    major_id: Optional[ObjectId] = field(default=None)
    program_id: Optional[ObjectId] = field(default=None)
    amount: int
    is_active: bool


class FinanceInvoicePriceVariantSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    price_id = ObjectIdField(required=True, allow_none=False)
    type_id = ObjectIdField(required=True, allow_none=False)
    gender = ma_fields.String(
        validate=validate.OneOf([None, "male", "female"]),
        required=False,
        allow_none=True,
    )
    is_boarding = ma_fields.Boolean(required=False, allow_none=True)
    is_alumni = ma_fields.Boolean(required=False, allow_none=True)
    degree_id = ObjectIdField(required=False, allow_none=True)
    major_id = ObjectIdField(required=False, allow_none=True)
    program_id = ObjectIdField(required=False, allow_none=True)
    amount = ma_fields.Integer(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceInvoicePriceVariant(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceInvoicePriceVariantData)
    collection_name = "finance_invoice_price_variant"
    schema = FinanceInvoicePriceVariantSchema
    search = ["gender", "amount"]
    object_class = FinanceInvoicePriceVariantData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "price": {
            "local": "price_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice_price"
            ).finance_invoice_price.FinanceInvoicePrice(),
        },
        "type": {
            "local": "type_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice_type"
            ).finance_invoice_type.FinanceInvoiceType(),
        },
        "degree": {
            "local": "degree_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_degree").edu_degree.EduDegree(),
        },
        "major": {
            "local": "major_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_major").edu_major.EduMajor(),
        },
        "program": {
            "local": "program_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_program").edu_program.EduProgram(),
        },
    }
