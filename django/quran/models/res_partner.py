from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass
class Address:
    street: str
    village: str
    district: str
    city: str
    province: str
    zipcode: str


class AddressSchema(Schema):
    street = ma_fields.String(required=True)
    village = ma_fields.String(required=True)
    district = ma_fields.String(required=True)
    city = ma_fields.String(required=True)
    province = ma_fields.String(required=True)
    zipcode = ma_fields.String(required=True)


@dataclass
class Location:
    type: str
    coordinates: List[float]


class LocationSchema(Schema):
    type = ma_fields.String(required=True)
    coordinates = ma_fields.List(ma_fields.Float(), required=True)


@dataclass(kw_only=True)
class ResPartnerData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    user_id: Optional[ObjectId] = field(default=None)
    name: str
    resident_no: Optional[str] = field(default=None)
    address: Address
    phone: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    website: Optional[str] = field(default=None)
    vat: Optional[str] = field(default=None)
    image: Optional[str] = field(default=None)
    customer_rank: Optional[int] = field(default=0)
    supplier_rank: Optional[int] = field(default=0)
    location: Optional[Location] = field(
        default_factory=lambda: {"type": "Point", "coordinates": [0, 0]}
    )
    is_customer: Optional[bool] = field(default=False)
    is_supplier: Optional[bool] = field(default=False)
    is_holding: Optional[bool] = field(default=False)
    is_school: Optional[bool] = field(default=False)
    is_staff: Optional[bool] = field(default=False)
    is_student: Optional[bool] = field(default=False)
    is_teacher: Optional[bool] = field(default=False)
    is_merchant: Optional[bool] = field(default=False)


class ResPartnerSchema(Schema):
    user_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    resident_no = ma_fields.String(required=False, allow_none=True)
    address = ma_fields.Nested(AddressSchema, required=True)
    phone = ma_fields.String(required=False, allow_none=True)
    email = ma_fields.String(required=False, allow_none=True)
    website = ma_fields.String(required=False, allow_none=True)
    vat = ma_fields.String(required=False, allow_none=True)
    image = ma_fields.String(required=False, allow_none=True)
    customer_rank = ma_fields.Integer(required=True)
    supplier_rank = ma_fields.Integer(required=True)
    location = ma_fields.Nested(LocationSchema, required=True)
    is_customer = ma_fields.Boolean(required=True)
    is_supplier = ma_fields.Boolean(required=True)
    is_holding = ma_fields.Boolean(required=True)
    is_school = ma_fields.Boolean(required=True)
    is_staff = ma_fields.Boolean(required=True)
    is_student = ma_fields.Boolean(required=True)
    is_teacher = ma_fields.Boolean(required=True)
    is_merchant = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ResPartner(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ResPartnerData)
    collection_name = "res_partner"
    schema = ResPartnerSchema
    search = ["name", "email", "phone"]
    object_class = ResPartnerData
    foreign_key = {
        "user": {
            "local": "user_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_user").res_user.ResUser(),
        }
    }
