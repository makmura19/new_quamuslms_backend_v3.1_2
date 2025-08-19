from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class EduMajorData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    origin: str
    name: str
    short_name: str


class EduMajorSchema(Schema):
    origin = ma_fields.String(validate=validate.OneOf(["vocational", "graduate"]), required=True)
    name = ma_fields.String(required=True)
    short_name = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class EduMajor(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(EduMajorData)
    collection_name = "edu_major"
    schema = EduMajorSchema
    search = ["origin", "name", "short_name"]
    object_class = EduMajorData
    foreign_key = {}
