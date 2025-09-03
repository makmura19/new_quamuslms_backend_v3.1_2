from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranReportTypeData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    code: str
    name: str
    description: str
    preview: Optional[str] = field(default=None)
    program_type: str


class QuranReportTypeSchema(Schema):
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)
    preview = ma_fields.String(required=False, allow_none=True)
    program_type = ma_fields.String(
        validate=validate.OneOf(["tahfidz", "tahsin", "pra_tahsin"]), required=True
    )
    _id = ObjectIdField(required=False, allow_none=True)


class QuranReportType(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranReportTypeData)
    collection_name = "quran_report_type"
    schema = QuranReportTypeSchema
    search = ["name", "description"]
    object_class = QuranReportTypeData
    foreign_key = {}
