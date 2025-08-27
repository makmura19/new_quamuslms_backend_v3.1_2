from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class FinanceNanoConfigData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    x_partner_id: str
    channel_id: str
    public_key: str
    is_active: bool


class FinanceNanoConfigSchema(Schema):
    x_partner_id = ma_fields.String(required=True)
    channel_id = ma_fields.String(required=True)
    public_key = ma_fields.String(required=True)
    is_active = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class FinanceNanoConfig(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(FinanceNanoConfigData)
    collection_name = "finance_nano_config"
    schema = FinanceNanoConfigSchema
    search = ["x_partner_id", "channel_id"]
    object_class = FinanceNanoConfigData
    foreign_key = {}
