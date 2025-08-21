from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil
from utils.string_util import StringUtil


@dataclass(kw_only=True)
class ResUserData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    student_id: Optional[ObjectId] = field(default=None)
    teacher_id: Optional[ObjectId] = field(default=None)
    employee_id: Optional[ObjectId] = field(default=None)
    merchant_id: Optional[ObjectId] = field(default=None)
    partner_id: Optional[ObjectId] = field(default=None)
    login: str
    password: Optional[str] = field(
        default_factory=lambda: StringUtil.generate_code("nnnnn")
    )
    name: str
    authority_id: Optional[ObjectId] = field(default=None)
    authority_ids: Optional[List[ObjectId]] = field(default_factory=list)
    authority_codes: Optional[List[str]] = field(default_factory=list)
    last_login: Optional[datetime] = field(default=None)
    is_staff: Optional[bool] = field(default=False)
    is_admin: Optional[bool] = field(default=False)
    is_staff_admin: Optional[bool] = field(default=False)
    is_password_encrypted: Optional[bool] = field(default=False)
    is_holding: Optional[bool] = field(default=False)
    is_school: Optional[bool] = field(default=False)
    is_student: Optional[bool] = field(default=False)
    is_teacher: Optional[bool] = field(default=False)
    is_merchant: Optional[bool] = field(default=False)
    is_active: Optional[bool] = field(default=True)


class ResUserSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    student_id = ObjectIdField(required=False, allow_none=True)
    teacher_id = ObjectIdField(required=False, allow_none=True)
    employee_id = ObjectIdField(required=False, allow_none=True)
    merchant_id = ObjectIdField(required=False, allow_none=True)
    partner_id = ObjectIdField(required=False, allow_none=True)
    login = ma_fields.String(required=True)
    password = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    authority_id = ObjectIdField(required=False, allow_none=True)
    authority_ids = ma_fields.List(ObjectIdField(), required=True)
    authority_codes = ma_fields.List(ma_fields.String(), required=True)
    last_login = ma_fields.DateTime(required=False, allow_none=True)
    is_staff = ma_fields.Boolean(required=True)
    is_admin = ma_fields.Boolean(required=True)
    is_staff_admin = ma_fields.Boolean(required=True)
    is_password_encrypted = ma_fields.Boolean(required=True)
    is_holding = ma_fields.Boolean(required=True)
    is_school = ma_fields.Boolean(required=True)
    is_student = ma_fields.Boolean(required=True)
    is_teacher = ma_fields.Boolean(required=True)
    is_merchant = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ResUser(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ResUserData)
    collection_name = "res_user"
    schema = ResUserSchema
    search = ["login", "name"]
    object_class = ResUserData
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
        "teacher": {
            "local": "teacher_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "employee": {
            "local": "employee_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.hr_employee").hr_employee.HrEmployee(),
        },
        "merchant": {
            "local": "merchant_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_merchant"
            ).finance_merchant.FinanceMerchant(),
        },
        "partner": {
            "local": "partner_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_partner").res_partner.ResPartner(),
        },
        "authority": {
            "local": "authority_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.res_authority"
            ).res_authority.ResAuthority(),
        },
    }

    def get_holding_username(self, _id, code, name):
        from utils.string_util import StringUtil
        from bson import ObjectId

        name = StringUtil.clean_text(name)
        while True:
            username = f"{code}_{StringUtil.get_initial(name)}{StringUtil.generate_code('nnnn')}"
            data = self.find_one({"holding_id": ObjectId(_id), "login": username})
            if not data:
                break
        return username

    def get_school_username(self, _id, code, name):
        from utils.string_util import StringUtil
        from bson import ObjectId

        name = StringUtil.clean_text(name)
        while True:
            username = f"{code}_{StringUtil.get_initial(name)}{StringUtil.generate_code('nnnn')}"
            data = self.find_one({"school_id": ObjectId(_id), "login": username})
            if not data:
                break
        return username
