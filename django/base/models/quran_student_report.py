from dataclasses import dataclass, field
from typing import Optional, List, Dict
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranStudentReportData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    student_id: ObjectId
    academic_year_id: ObjectId
    semester_id: ObjectId
    notes: str
    attendance: Dict[str, int]
    type: int
    line_group: Optional[List[str]] = field(default_factory=list)
    line_ids: Optional[List[ObjectId]] = field(default_factory=list)
    report_type_id: ObjectId


class QuranStudentReportSchema(Schema):
    school_id = ObjectIdField(required=True)
    student_id = ObjectIdField(required=True)
    academic_year_id = ObjectIdField(required=True)
    semester_id = ObjectIdField(required=True)
    notes = ma_fields.String(required=True)
    attendance = ma_fields.Dict(
        keys=ma_fields.String(), values=ma_fields.Integer(), required=True
    )
    type = ma_fields.Integer(required=True)
    line_group = ma_fields.List(ma_fields.String(), required=True)
    line_ids = ma_fields.List(ObjectIdField(), required=True)
    report_type_id = ObjectIdField(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranStudentReport(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranStudentReportData)
    collection_name = "quran_student_report"
    schema = QuranStudentReportSchema
    search = ["notes", "line_group", "type"]
    object_class = QuranStudentReportData
    foreign_key = {
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
        "academic_year": {
            "local": "academic_year_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_academic_year"
            ).edu_academic_year.EduAcademicYear(),
        },
        "semester": {
            "local": "semester_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.edu_semester"
            ).edu_semester.EduSemester(),
        },
        "lines": {
            "local": "line_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_report_line"
            ).quran_report_line.QuranReportLine(),
        },
        "report_type": {
            "local": "report_type_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_report_type"
            ).quran_report_type.QuranReportType(),
        },
    }
