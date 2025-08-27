from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceNanoExternalIdData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    external_id: str
    date: datetime


class FinanceNanoExternalIdSchema(Schema):
    external_id = ma_fields.String(required=True)
    date = ma_fields.DateTime(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceNanoExternalId(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceNanoExternalIdData)
    collection_name = "finance_nano_external_id"
    schema = FinanceNanoExternalIdSchema
    search = ["external_id", "date"]
    object_class = FinanceNanoExternalIdData
    foreign_key = {}
