from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class StudentInfoData:
    academic_class: bool
    quran_class: bool
    teacher: bool
    semester: bool
    academic_year: bool
    nis: bool
    nisn: bool
    order: List[str]


class StudentInfoSchema(Schema):
    academic_class = ma_fields.Boolean(required=True)
    quran_class = ma_fields.Boolean(required=True)
    teacher = ma_fields.Boolean(required=True)
    semester = ma_fields.Boolean(required=True)
    academic_year = ma_fields.Boolean(required=True)
    nis = ma_fields.Boolean(required=True)
    nisn = ma_fields.Boolean(required=True)
    order = ma_fields.List(ma_fields.String(), required=True)


@dataclass(kw_only=True)
class HeaderData:
    school_logo: bool
    quamus_logo: bool
    holding_logo: bool
    address: bool
    title: bool
    periodic_title: bool
    academic_year: bool
    order: List[str]


class HeaderSchema(Schema):
    school_logo = ma_fields.Boolean(required=True)
    quamus_logo = ma_fields.Boolean(required=True)
    holding_logo = ma_fields.Boolean(required=True)
    address = ma_fields.Boolean(required=True)
    title = ma_fields.Boolean(required=True)
    periodic_title = ma_fields.Boolean(required=True)
    academic_year = ma_fields.Boolean(required=True)
    order = ma_fields.List(ma_fields.String(), required=True)


@dataclass(kw_only=True)
class SignatureData:
    principal: bool
    coordinator: bool
    parent: bool
    quamus: bool


class SignatureSchema(Schema):
    principal = ma_fields.Boolean(required=True)
    coordinator = ma_fields.Boolean(required=True)
    parent = ma_fields.Boolean(required=True)
    quamus = ma_fields.Boolean(required=True)


@dataclass(kw_only=True)
class LabelData:
    principal: str
    coordinator: str
    parent: str
    title: str
    periodic_title: str
    place: str
    address: str


class LabelSchema(Schema):
    principal = ma_fields.String(required=True)
    coordinator = ma_fields.String(required=True)
    parent = ma_fields.String(required=True)
    title = ma_fields.String(required=True)
    periodic_title = ma_fields.String(required=True)
    place = ma_fields.String(required=True)
    address = ma_fields.String(required=True)


@dataclass(kw_only=True)
class ComponentScoreData:
    is_daily: bool
    is_exam: bool


class ComponentScoreSchema(Schema):
    is_daily = ma_fields.Boolean(required=True)
    is_exam = ma_fields.Boolean(required=True)


@dataclass(kw_only=True)
class ReportRubricData:
    letter: str
    name: str
    gte: int
    lte: int


class ReportRubricSchema(Schema):
    letter = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    gte = ma_fields.Integer(required=True)
    lte = ma_fields.Integer(required=True)


@dataclass(kw_only=True)
class ConfigQuranReportData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    student_info: StudentInfoData
    header: HeaderData
    signature: SignatureData
    label: LabelData
    use_chapter_recap: bool
    total_rule: Optional[str] = field(default=None)
    component_score: ComponentScoreData
    report_rubric: List[ReportRubricData]
    type_id: ObjectId


class ConfigQuranReportSchema(Schema):
    school_id = ObjectIdField(required=True)
    student_info = ma_fields.Nested(StudentInfoSchema, required=True)
    header = ma_fields.Nested(HeaderSchema, required=True)
    signature = ma_fields.Nested(SignatureSchema, required=True)
    label = ma_fields.Nested(LabelSchema, required=True)
    use_chapter_recap = ma_fields.Boolean(required=True)
    total_rule = ma_fields.String(
        validate=validate.OneOf([None, "accumulative", "average"]),
        allow_none=True,
        required=False,
    )
    component_score = ma_fields.Nested(ComponentScoreSchema, required=True)
    report_rubric = ma_fields.List(ma_fields.Nested(ReportRubricSchema), required=True)
    type_id = ObjectIdField(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class ConfigQuranReport(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ConfigQuranReportData)
    collection_name = "config_quran_report"
    schema = ConfigQuranReportSchema
    search = ["school_id", "type_id"]
    object_class = ConfigQuranReportData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "type": {
            "local": "type_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_report_type"
            ).quran_report_type.QuranReportType(),
        },
    }
