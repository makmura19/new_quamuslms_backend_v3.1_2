from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class AccountAccountData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    holding_id: Optional[ObjectId] = field(default=None)
    school_id: Optional[ObjectId] = field(default=None)
    code: str
    name: str
    type: str
    group: str
    parent_id: Optional[ObjectId] = field(default=None)
    child_ids: Optional[List[ObjectId]] = field(default_factory=list)
    sequence: int
    note: str
    display_name: str
    is_active: Optional[bool] = field(default=True)
    is_manual: Optional[bool] = field(default=True)
    is_group: Optional[bool] = field(default=False)
    is_template: Optional[bool] = field(default=False)
    is_postable: Optional[bool] = field(default=False)


class AccountAccountSchema(Schema):
    holding_id = ObjectIdField(required=False, allow_none=True)
    school_id = ObjectIdField(required=False, allow_none=True)
    code = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    type = ma_fields.String(
        validate=validate.OneOf(["asset", "liability", "income", "expense", "equity"]),
        required=True,
    )
    group = ma_fields.String(
        validate=validate.OneOf(
            [
                "bank",
                "cash",
                "student_receivable",
                "vendor_payable",
                "merchant_payable",
                "student_saving_payable",
                "parent_refund_payable",
                "tuition_income",
                "donation_income",
                "operational_expense",
                "salary_expense",
                "teaching_material_expense",
                "other",
            ]
        ),
        required=True,
    )
    parent_id = ObjectIdField(required=False, allow_none=True)
    child_ids = ma_fields.List(ObjectIdField(), required=True)
    sequence = ma_fields.Integer(required=True)
    note = ma_fields.String(required=True)
    display_name = ma_fields.String(required=True)
    is_active = ma_fields.Boolean(required=True)
    is_manual = ma_fields.Boolean(required=True)
    is_group = ma_fields.Boolean(required=True)
    is_template = ma_fields.Boolean(required=True)
    is_postable = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class AccountAccount(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(AccountAccountData)
    collection_name = "account_account"
    schema = AccountAccountSchema
    search = ["code", "name", "display_name"]
    object_class = AccountAccountData
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
        "parent": {
            "local": "parent_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
        "child": {
            "local": "child_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.account_account"
            ).account_account.AccountAccount(),
        },
    }


    def get_code(self, parent_code, holding_id, school_id):
        existing_data = self.get_parent(parent_code, holding_id, school_id)
        if not existing_data:
            return None
        child_ids = [ObjectId(i) for i in existing_data.get("child_ids")]
        if child_ids:
            child_data = self.find({"_id":{"$in":child_ids}})
            child_code = [int(i.get("code")) for i in child_data]
            last_code = max(child_code) + 1
        else:
            last_code = int(parent_code)+1
        return f"{last_code}", existing_data

    def get_parent(self, parent_code, holding_id, school_id):
        query = {"code": parent_code}
        if holding_id:
            query["holding_id"] = holding_id
        else:
            query["school_id"] = school_id
        existing_data = self.find_one(query)
        return existing_data

    def create_account(self, parent_code, holding_id, school_id, name, user=None):
        from models.school_school import SchoolSchool
        map = {
            "tuition_income": "Pendapatan",
            "student_receivable": "Piutang",
            "bank": "Bank",
            "merchant_payable": "Utang Merchant",
            "vendor_payable": "Utang Quamus",
            "cash": "Kas",
        }

        _id = ObjectId()
        account_name = ""
        income_code, parent_data = self.get_code(parent_code, holding_id, school_id)
        parent_id = ObjectId(parent_data.get("_id"))
        if school_id:
            school_data = SchoolSchool().find_one({"_id": school_id})
            account_name = []
            if map.get(parent_data.get("group")):
                account_name.append(map.get(parent_data.get("group")))
            if name:
                account_name.append(name)
            if parent_data.get("group") not in [
                "bank",
                "merchant_payable",
            ] and school_data.get("name"):
                account_name.append(school_data.get("name"))
            account_name = " ".join(account_name)
        else:
            account_name = name
        
        item_ = {
            "_id": _id,
            "holding_id": holding_id,
            "school_id": school_id,
            "code": income_code,
            "name": account_name,
            "type": parent_data.get("type"),
            "group": parent_data.get("group"),
            "is_active": True,
            "is_manual": False,
            "parent_id": parent_id,
            "child_ids": [],
            "sequence": 0,
            "note": "",
            "display_name": f"{income_code} - {account_name}",
            "is_template": False,
            "is_group": False,
            "is_postable": True,
        }
        self.insert_one(item_, user=user)
        self.update_one(
            {"_id": parent_id},
            add_to_set_data={"child_ids": _id},
            user=user,
        )
        return _id