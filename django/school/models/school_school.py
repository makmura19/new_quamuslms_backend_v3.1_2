from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SummaryData:
    parent_balance: int
    pocket_balance: int
    quamus_balance: int
    merchant_balance: int
    unpaid_invoice: int
    male_student_count: int
    female_student_count: int
    male_teacher_count: int
    female_teacher_count: int


@dataclass(kw_only=True)
class SchoolSchoolData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    stage_id: ObjectId
    stage_group_id: ObjectId
    stage_group_level: int
    partner_id: ObjectId
    code: str
    name: str
    display_name: Optional[str] = field(default="")
    npsn: str
    subject_ids: Optional[List[ObjectId]] = field(default_factory=list)
    module_ids: Optional[List[ObjectId]] = field(default_factory=list)
    module_codes: Optional[List[str]] = field(default_factory=list)
    degree_ids: Optional[List[ObjectId]] = field(default_factory=list)
    faculty_ids: Optional[List[ObjectId]] = field(default_factory=list)
    major_ids: Optional[List[ObjectId]] = field(default_factory=list)
    program_ids: Optional[List[ObjectId]] = field(default_factory=list)
    dormitory_ids: Optional[List[ObjectId]] = field(default_factory=list)
    group_ids: Optional[List[ObjectId]] = field(default_factory=list)
    tz: Optional[str] = field(default="Asia/Jakarta")
    logo_sm: Optional[str] = field(default=None)
    logo_md: Optional[str] = field(default=None)
    logo_hd: Optional[str] = field(default=None)
    config_mutabaah_id: Optional[ObjectId] = field(default=None)
    config_finance_id: Optional[ObjectId] = field(default=None)
    config_lms_id: Optional[ObjectId] = field(default=None)
    config_tahfidz_id: Optional[ObjectId] = field(default=None)
    config_tashin_id: Optional[ObjectId] = field(default=None)
    config_pratahsin_id: Optional[ObjectId] = field(default=None)
    config_va_ids: Optional[List[ObjectId]] = field(default_factory=list)
    join_date: Optional[datetime] = field(default=None)
    expired_at: Optional[datetime] = field(default=None)
    staff_ids: Optional[List[ObjectId]] = field(default_factory=list)
    contact_ids: Optional[List[ObjectId]] = field(default_factory=list)
    summary: Optional[SummaryData] = field(
        default_factory=lambda: {
            "parent_balance": 0,
            "pocket_balance": 0,
            "quamus_balance": 0,
            "merchant_balance": 0,
            "unpaid_invoice": 0,
            "male_student_count": 0,
            "female_student_count": 0,
            "male_teacher_count": 0,
            "female_teacher_count": 0,
        }
    )
    payable_id: Optional[ObjectId] = field(default=None)
    cash_id: Optional[ObjectId] = field(default=None)
    is_boarding: Optional[bool] = field(default=False)
    under_holding: Optional[bool] = field(default=False)
    is_account_created: Optional[bool] = field(default=False)
    is_subject_created: Optional[bool] = field(default=False)
    marketing_status: Optional[str] = field(default=None)
    implement_status: Optional[str] = field(default=None)
    subscription_status: Optional[str] = field(default=None)
    is_client: Optional[bool] = field(default=False)
    extracurricular_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_active: Optional[bool] = field(default=False)


class SummarySchema(Schema):
    parent_balance = ma_fields.Integer(required=True)
    pocket_balance = ma_fields.Integer(required=True)
    quamus_balance = ma_fields.Integer(required=True)
    merchant_balance = ma_fields.Integer(required=True)
    unpaid_invoice = ma_fields.Integer(required=True)
    male_student_count = ma_fields.Integer(required=True)
    female_student_count = ma_fields.Integer(required=True)
    male_teacher_count = ma_fields.Integer(required=True)
    female_teacher_count = ma_fields.Integer(required=True)


class SchoolSchoolSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    stage_id = ObjectIdField(required=True, allow_none=False)
    stage_group_id = ObjectIdField(required=True, allow_none=False)
    stage_group_level = ma_fields.Integer(required=True)
    partner_id = ObjectIdField(required=True, allow_none=False)
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    display_name = ma_fields.String(required=True)
    npsn = ma_fields.String(required=True)
    subject_ids = ma_fields.List(ObjectIdField(), required=True)
    module_ids = ma_fields.List(ObjectIdField(), required=True)
    module_codes = ma_fields.List(ma_fields.String(), required=True)
    degree_ids = ma_fields.List(ObjectIdField(), required=True)
    faculty_ids = ma_fields.List(ObjectIdField(), required=True)
    major_ids = ma_fields.List(ObjectIdField(), required=True)
    program_ids = ma_fields.List(ObjectIdField(), required=True)
    dormitory_ids = ma_fields.List(ObjectIdField(), required=True)
    group_ids = ma_fields.List(ObjectIdField(), required=True)
    tz = ma_fields.String(
        validate=validate.OneOf(["Asia/Jakarta", "Asia/Makasar", "Asia/Jayapura"]),
        required=True,
    )
    logo_sm = ma_fields.String(required=False, allow_none=True)
    logo_md = ma_fields.String(required=False, allow_none=True)
    logo_hd = ma_fields.String(required=False, allow_none=True)
    config_mutabaah_id = ObjectIdField(required=False, allow_none=True)
    config_finance_id = ObjectIdField(required=False, allow_none=True)
    config_lms_id = ObjectIdField(required=False, allow_none=True)
    config_tahfidz_id = ObjectIdField(required=False, allow_none=True)
    config_tashin_id = ObjectIdField(required=False, allow_none=True)
    config_pratahsin_id = ObjectIdField(required=False, allow_none=True)
    config_va_ids = ma_fields.List(ObjectIdField(), required=True)
    join_date = ma_fields.DateTime(required=False, allow_none=True)
    expired_at = ma_fields.DateTime(required=False, allow_none=True)
    staff_ids = ma_fields.List(ObjectIdField(), required=True)
    contact_ids = ma_fields.List(ObjectIdField(), required=True)
    summary = ma_fields.Nested(SummarySchema, required=True)
    payable_id = ObjectIdField(required=False, allow_none=True)
    cash_id = ObjectIdField(required=False, allow_none=True)
    is_boarding = ma_fields.Boolean(required=True)
    under_holding = ma_fields.Boolean(required=True)
    is_account_created = ma_fields.Boolean(required=True)
    is_subject_created = ma_fields.Boolean(required=True)
    marketing_status = ma_fields.String(
        required=False,
        allow_none=True,
        validate=validate.OneOf(
            ["lead", "contacted", "visited", "approaching_mou", "mou_signed", "loss"]
        ),
    )
    implement_status = ma_fields.String(
        required=False,
        allow_none=True,
        validate=validate.OneOf(
            ["data_gathering", "training", "onboarding", "live", "suspended", "closed"]
        ),
    )
    subscription_status = ma_fields.String(
        required=False,
        allow_none=True,
        validate=validate.OneOf(
            ["trial", "active", "expired", "non_renewed", "terminated"]
        ),
    )
    is_client = ma_fields.Boolean(required=True)
    extracurricular_ids = ma_fields.List(ObjectIdField(), required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolSchool(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolSchoolData)
    collection_name = "school_school"
    schema = SchoolSchoolSchema
    search = ["code", "name", "display_name", "npsn", "module_codes"]
    object_class = SchoolSchoolData
    foreign_key = {
        "holding": {
            "local": "holding_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_holding"
            ).school_holding.SchoolHolding(),
        },
        "stage": {
            "local": "stage_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_stage").edu_stage.EduStage(),
        },
        "stage_group": {
            "local": "stage_group_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_stage_group"
            ).edu_stage_group.EduStageGroup(),
        },
        "partner": {
            "local": "partner_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_partner").res_partner.ResPartner(),
        },
        "subjects": {
            "local": "subject_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_subject"
            ).school_subject.SchoolSubject(),
        },
        "modules": {
            "local": "module_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_module"
            ).school_module.SchoolModule(),
        },
        "degrees": {
            "local": "degree_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_degree").edu_degree.EduDegree(),
        },
        "faculties": {
            "local": "faculty_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_faculty"
            ).school_faculty.SchoolFaculty(),
        },
        "majors": {
            "local": "major_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_major").edu_major.EduMajor(),
        },
        "programs": {
            "local": "program_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_program").edu_program.EduProgram(),
        },
        "dormitories": {
            "local": "dormitory_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_dormitory"
            ).school_dormitory.SchoolDormitory(),
        },
        "groups": {
            "local": "group_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_group"
            ).school_group.SchoolGroup(),
        },
        "config_mutabaah": {
            "local": "config_mutabaah_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.config_mutabaah"
            ).config_mutabaah.ConfigMutabaah(),
        },
        "config_finance": {
            "local": "config_finance_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.config_finance"
            ).config_finance.ConfigFinance(),
        },
        "config_lms": {
            "local": "config_lms_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.config_lms").config_lms.ConfigLms(),
        },
        "config_tahfidz": {
            "local": "config_tahfidz_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.config_tahfidz"
            ).config_tahfidz.ConfigTahfidz(),
        },
        "config_tashin": {
            "local": "config_tashin_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.config_tahsin"
            ).config_tahsin.ConfigTahsin(),
        },
        "config_pratahsin": {
            "local": "config_pratahsin_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.config_pratahsin"
            ).config_pratahsin.ConfigPratahsin(),
        },
        "config_vas": {
            "local": "config_va_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_va_config"
            ).finance_va_config.FinanceVaConfig(),
        },
        "staffs": {
            "local": "staff_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_staff"
            ).school_staff.SchoolStaff(),
        },
        "contacts": {
            "local": "contact_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_partner").res_partner.ResPartner(),
        },
        "payable": {
            "local": "payable_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
        "cash": {
            "local": "cash_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
        "extracurriculars": {
            "local": "extracurricular_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_degree").edu_degree.EduDegree(),
        },
    }

    def get_code(self):
        from utils.string_util import StringUtil

        while True:
            code = StringUtil.generate_code("nnnnn")
            data = self.find_one({"code": code})
            if not data:
                break
        return code
