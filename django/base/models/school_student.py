from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SchoolStudentData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: ObjectId
    name: str
    gender: str
    nis: str
    nisn: str
    user_id: Optional[ObjectId] = field(default=None)
    login: Optional[str] = field(default=None)
    class_academic_year_id: Optional[ObjectId] = field(default=None)
    class_id: Optional[ObjectId] = field(default=None)
    class_history_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_alumni: bool
    is_boarding: bool
    student_book_id: Optional[ObjectId] = field(default=None)
    join_academic_year_id: Optional[ObjectId] = field(default=None)
    birth_date: Optional[datetime] = field(default=None)
    birth_place: Optional[str] = field(default=None)
    program_id: Optional[ObjectId] = field(default=None)
    major_id: Optional[ObjectId] = field(default=None)
    degree_id: Optional[ObjectId] = field(default=None)
    stage_group_id: Optional[ObjectId] = field(default=None)
    stage_id: Optional[ObjectId] = field(default=None)
    level_id: Optional[ObjectId] = field(default=None)
    dormitory_id: Optional[ObjectId] = field(default=None)
    dormitory_room_id: Optional[ObjectId] = field(default=None)
    is_graduated: bool
    graduated_at: Optional[datetime] = field(default=None)
    qrcode: str
    pin: str
    parent_balance: Optional[int] = field(default=0)
    pocket_balance: Optional[int] = field(default=0)
    pocket_treshold: Optional[int] = field(default=0)
    main_va: Optional[str] = field(default=None)
    va_ids: Optional[List[ObjectId]] = field(default_factory=list)
    va_nos: Optional[List[str]] = field(default_factory=list)
    unpaid_invoice_ids: Optional[List[ObjectId]] = field(default_factory=list)
    unpaid_total: Optional[int] = field(default=0)
    photo: Optional[str] = field(default=None)
    phone: Optional[str] = field(default=None)
    quran_class_ids: Optional[List[ObjectId]] = field(default_factory=list)


class SchoolStudentSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=True)
    name = ma_fields.String(required=True)
    gender = ma_fields.String(
        validate=validate.OneOf(["male", "female"]), required=True
    )
    nis = ma_fields.String(required=True)
    nisn = ma_fields.String(required=True)
    user_id = ObjectIdField(required=False, allow_none=True)
    login = ma_fields.String(required=False, allow_none=True)
    class_academic_year_id = ObjectIdField(required=False, allow_none=True)
    class_id = ObjectIdField(required=False, allow_none=True)
    class_history_ids = ma_fields.List(ObjectIdField(), required=True)
    is_alumni = ma_fields.Boolean(required=True)
    is_boarding = ma_fields.Boolean(required=True)
    student_book_id = ObjectIdField(required=False, allow_none=True)
    join_academic_year_id = ObjectIdField(required=False, allow_none=True)
    birth_date = ma_fields.DateTime(required=False, allow_none=True)
    birth_place = ma_fields.String(required=False, allow_none=True)
    program_id = ObjectIdField(required=False, allow_none=True)
    major_id = ObjectIdField(required=False, allow_none=True)
    degree_id = ObjectIdField(required=False, allow_none=True)
    stage_group_id = ObjectIdField(required=False, allow_none=True)
    stage_id = ObjectIdField(required=False, allow_none=True)
    level_id = ObjectIdField(required=False, allow_none=True)
    dormitory_id = ObjectIdField(required=False, allow_none=True)
    dormitory_room_id = ObjectIdField(required=False, allow_none=True)
    is_graduated = ma_fields.Boolean(required=True)
    graduated_at = ma_fields.DateTime(required=False, allow_none=True)
    qrcode = ma_fields.String(required=True)
    pin = ma_fields.String(required=True)
    parent_balance = ma_fields.Integer(required=True)
    pocket_balance = ma_fields.Integer(required=True)
    pocket_treshold = ma_fields.Integer(required=True)
    main_va = ma_fields.String(required=False, allow_none=True)
    va_ids = ma_fields.List(ObjectIdField(), required=True)
    va_nos = ma_fields.List(ma_fields.String(), required=True)
    unpaid_invoice_ids = ma_fields.List(ObjectIdField(), required=True)
    unpaid_total = ma_fields.Integer(required=True)
    photo = ma_fields.String(required=False, allow_none=True)
    phone = ma_fields.String(required=False, allow_none=True)
    quran_class_ids = ma_fields.List(ObjectIdField(), required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class SchoolStudent(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(SchoolStudentData)
    collection_name = "school_student"
    schema = SchoolStudentSchema
    search = ["name", "nis", "nisn", "phone"]
    object_class = SchoolStudentData
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
        "user": {
            "local": "user_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.res_user").res_user.ResUser(),
        },
        "class_academic_year": {
            "local": "class_academic_year_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_academic_year"
            ).edu_academic_year.EduAcademicYear(),
        },
        "class": {
            "local": "class_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_class"
            ).school_class.SchoolClass(),
        },
        "class_history": {
            "local": "class_history_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_class"
            ).school_class.SchoolClass(),
        },
        "student_book": {
            "local": "student_book_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_student_book"
            ).school_student_book.SchoolStudentBook(),
        },
        "join_academic_year": {
            "local": "join_academic_year_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_academic_year"
            ).edu_academic_year.EduAcademicYear(),
        },
        "program": {
            "local": "program_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_program").edu_program.EduProgram(),
        },
        "major": {
            "local": "major_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_major").edu_major.EduMajor(),
        },
        "degree": {
            "local": "degree_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_degree").edu_degree.EduDegree(),
        },
        "stage_group": {
            "local": "stage_group_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_stage_group"
            ).edu_stage_group.EduStageGroup(),
        },
        "stage": {
            "local": "stage_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_stage").edu_stage.EduStage(),
        },
        "level": {
            "local": "level_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.edu_level").edu_level.EduLevel(),
        },
        "dormitory": {
            "local": "dormitory_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_dormitory"
            ).school_dormitory.SchoolDormitory(),
        },
        "dormitory_room": {
            "local": "dormitory_room_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_dormitory_room"
            ).school_dormitory_room.SchoolDormitoryRoom(),
        },
        "main_va": {
            "local": "main_va",
            "foreign": "va_no",
            "sort": None,
            "model": lambda: __import__("models.finance_va").finance_va.FinanceVa(),
        },
        "va": {
            "local": "va_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.finance_va").finance_va.FinanceVa(),
        },
        "unpaid_invoice": {
            "local": "unpaid_invoice_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.finance_invoice"
            ).finance_invoice.FinanceInvoice(),
        },
        "quran_class": {
            "local": "quran_class_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_class").quran_class.QuranClass(),
        },
    }
