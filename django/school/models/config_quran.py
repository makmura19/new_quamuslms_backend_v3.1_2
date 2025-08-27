from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class SignatureData:
    is_principal: bool
    is_coordinator: bool
    is_parent: bool


class SignatureSchema(Schema):
    is_principal = ma_fields.Boolean(required=True)
    is_coordinator = ma_fields.Boolean(required=True)
    is_parent = ma_fields.Boolean(required=True)


@dataclass(kw_only=True)
class ConfigQuranData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    report_config_id: ObjectId
    daily_assesment_rule: str
    exam_assesment_rule: str
    juziyah_assesment_rule: str
    signature: SignatureData
    coordinator_id: ObjectId
    teacher_ids: Optional[List[ObjectId]] = field(default_factory=list)
    target_period: Optional[str] = field(default=None)
    exam_threshold: Optional[int] = field(default=None)
    use_matrix: bool
    multiple_class_per_student: bool
    program_type: str
    use_whatsapp: bool
    whatsapp_no: Optional[str] = field(default=None)
    quran_type: str
    is_active: Optional[bool] = field(default=True)


class ConfigQuranSchema(Schema):
    school_id = ObjectIdField(required=True)
    report_config_id = ObjectIdField(required=True)
    daily_assesment_rule = ma_fields.String(
        validate=validate.OneOf(["type_1", "type_2"]), required=True
    )
    exam_assesment_rule = ma_fields.String(
        validate=validate.OneOf(["type_1", "type_2"]), required=True
    )
    juziyah_assesment_rule = ma_fields.String(
        validate=validate.OneOf(["type_1", "type_2"]), required=True
    )
    signature = ma_fields.Nested(SignatureSchema, required=True)
    coordinator_id = ObjectIdField(required=True)
    teacher_ids = ma_fields.List(ObjectIdField(), required=True)
    target_period = ma_fields.String(
        validate=validate.OneOf([None, "semester", "year", "full"]),
        allow_none=True,
        required=False,
    )
    exam_threshold = ma_fields.Integer(required=False, allow_none=True)
    use_matrix = ma_fields.Boolean(required=True)
    multiple_class_per_student = ma_fields.Boolean(required=True)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    use_whatsapp = ma_fields.Boolean(required=True)
    whatsapp_no = ma_fields.String(required=False, allow_none=True)
    quran_type = ma_fields.String(
        validate=validate.OneOf(["madinah", "kemenag"]), required=True
    )
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ConfigQuran(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ConfigQuranData)
    collection_name = "config_quran"
    schema = ConfigQuranSchema
    search = ["school_id", "program_type", "quran_type"]
    object_class = ConfigQuranData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "report_config": {
            "local": "report_config_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.config_quran_report"
            ).config_quran_report.ConfigQuranReport(),
        },
        "coordinator": {
            "local": "coordinator_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "teachers": {
            "local": "teacher_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
    }
