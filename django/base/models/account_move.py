from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class AccountMoveData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    name: str
    ref: str
    line_ids: Optional[List[ObjectId]] = field(default_factory=list)
    state: str
    posted_date: Optional[datetime] = field(default=None)
    is_auto_generated: bool
    date: datetime
    staff_id: Optional[ObjectId] = field(default=None)
    note: str


class AccountMoveSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    name = ma_fields.String(required=True)
    ref = ma_fields.String(required=True)
    line_ids = ma_fields.List(ObjectIdField(), required=True)
    state = ma_fields.String(
        validate=validate.OneOf(["draft", "posted", "cancel"]), required=True
    )
    posted_date = ma_fields.DateTime(required=False, allow_none=True)
    is_auto_generated = ma_fields.Boolean(required=True)
    date = ma_fields.DateTime(required=True)
    staff_id = ObjectIdField(required=False, allow_none=True)
    note = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class AccountMove(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(AccountMoveData)
    collection_name = "account_move"
    schema = AccountMoveSchema
    search = ["name", "ref", "state"]
    object_class = AccountMoveData
    foreign_key = {
        "holding": {
            "local": "holding_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_holding"
            ).school_holding.SchoolHolding(),
        },
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        },
        "lines": {
            "local": "line_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_move_line"
            ).account_move_line.AccountMoveLine(),
        },
        "staff": {
            "local": "staff_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_staff"
            ).school_staff.SchoolStaff(),
        },
    }
