from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class CbtPackageData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    teacher_id: ObjectId
    subject_id: ObjectId
    level_id: ObjectId
    name: str
    question_ids: Optional[List[ObjectId]] = field(default_factory=list)
    is_public: bool
    is_active: Optional[bool] = field(default=True)


class CbtPackageSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    teacher_id = ObjectIdField(required=True, allow_none=False)
    subject_id = ObjectIdField(required=True, allow_none=False)
    level_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    question_ids = ma_fields.List(ObjectIdField(), required=True)
    is_public = ma_fields.Boolean(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class CbtPackage(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(CbtPackageData)
    collection_name = "cbt_package"
    schema = CbtPackageSchema
    search = ["name"]
    object_class = CbtPackageData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "teacher": {
            "local": "teacher_id",
            "foreign": "_id",
            "sort": None,
            "fields" : "_id,name",
            "model": lambda: __import__(
                "models.school_teacher"
            ).school_teacher.SchoolTeacher(),
        },
        "subject": {
            "local": "subject_id",
            "foreign": "_id",
            "sort": None,
            "fields" : "_id,name",
            "model": lambda: __import__(
                "models.school_subject"
            ).school_subject.SchoolSubject(),
        },
        "level": {
            "local": "level_id",
            "foreign": "_id",
            "sort": None,
            "fields" : "_id,name",
            "model": lambda: __import__(
                "models.edu_stage_level"
            ).edu_stage_level.EduStageLevel(),
        },
        "questions": {
            "local": "question_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.cbt_package_question"
            ).cbt_package_question.CbtPackageQuestion(),
        },
    }
