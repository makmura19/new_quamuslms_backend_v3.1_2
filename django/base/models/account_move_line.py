from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class AccountMoveLineData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: ObjectId
    school_id: ObjectId
    move_id: ObjectId
    student_id: Optional[ObjectId] = field(default=None)
    coa_id: ObjectId
    name: str
    debit: int
    credit: int
    is_reconciled: bool
    note: str
    staff_id: Optional[ObjectId] = field(default=None)


class AccountMoveLineSchema(Schema):
    holding_id = ObjectIdField(required=True, allow_none=False)
    school_id = ObjectIdField(required=True, allow_none=False)
    move_id = ObjectIdField(required=True, allow_none=False)
    student_id = ObjectIdField(required=False, allow_none=True)
    coa_id = ObjectIdField(required=True, allow_none=False)
    name = ma_fields.String(required=True)
    debit = ma_fields.Integer(required=True)
    credit = ma_fields.Integer(required=True)
    is_reconciled = ma_fields.Boolean(required=True)
    note = ma_fields.String(required=True)
    staff_id = ObjectIdField(required=False, allow_none=True)
    _id = ObjectIdField(required=False, allow_none=True)


class AccountMoveLine(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(AccountMoveLineData)
    collection_name = "account_move_line"
    schema = AccountMoveLineSchema
    search = ["name", "note"]
    object_class = AccountMoveLineData
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
        "move": {
            "local": "move_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_move"
            ).account_move.AccountMove(),
        },
        "coa": {
            "local": "coa_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
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
