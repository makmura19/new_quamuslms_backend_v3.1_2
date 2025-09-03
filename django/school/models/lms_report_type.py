from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class LmsReportTypeData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    code: str
    name: str
    description: str
    preview: Optional[str] = field(default=None)


class LmsReportTypeSchema(Schema):
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    preview = ma_fields.String(required=False, allow_none=True)
    _id = ObjectIdField(required=False, allow_none=True)


class LmsReportType(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(LmsReportTypeData)
    collection_name = "lms_report_type"
    schema = LmsReportTypeSchema
    search = ["code", "name", "description"]
    object_class = LmsReportTypeData
    foreign_key = {}
