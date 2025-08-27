from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranStudentPageData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    student_id: ObjectId
    page_id: ObjectId
    page_seq: int
    list: List[str]


class QuranStudentPageSchema(Schema):
    school_id = ObjectIdField(required=True)
    student_id = ObjectIdField(required=True)
    page_id = ObjectIdField(required=True)
    page_seq = ma_fields.Integer(required=True)
    list = ma_fields.List(ma_fields.String(), required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranStudentPage(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranStudentPageData)
    collection_name = "quran_student_page"
    schema = QuranStudentPageSchema
    search = ["page_seq", "list"]
    object_class = QuranStudentPageData
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
        "page": {
            "local": "page_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_page").quran_page.QuranPage(),
        },
    }
