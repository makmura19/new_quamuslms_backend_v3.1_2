from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId
import json
from models.finance_va_config import FinanceVaConfig, FinanceVaConfigData
from models.account_account import AccountAccount
from models.school_school import SchoolSchool
from models.school_holding import SchoolHolding


class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        existing = FinanceVaConfig().find_one({
            "bank_id": ObjectId(value.get("bank_id")),
            "vendor_id": ObjectId(value.get("vendor_id")),
            "holding_id": ObjectId(value.get("holding_id")) if value.get("holding_id") else None,
            "school_id": ObjectId(value.get("school_id")) if value.get("school_id") else None
        })
        if existing:
            raise ValidationError("Data VA config sudah ada.")

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        school_id = ObjectId(validated_data.get("school_id")) if validated_data.get("school_id") else None
        holding_id=ObjectId(validated_data.get("holding_id")) if validated_data.get("holding_id") else None
        name = f"{extra.get('res_bank',{}).get('short_name')} {validated_data.get('account_no')} An. {validated_data.get('account_name')}{validated_data.get('purpose')}"
        
        bank_coa_id = AccountAccount().create_account("1200", holding_id, school_id, name, user)
        
        new_va_config_data = FinanceVaConfigData(
            bank_id=ObjectId(validated_data.get("bank_id")),
            vendor_id=ObjectId(validated_data.get("vendor_id")),
            coa_id=bank_coa_id,
            holding_id=ObjectId(validated_data.get("holding_id")) if validated_data.get("holding_id") else None,
            school_id=ObjectId(validated_data.get("school_id")) if validated_data.get("school_id") else None,
            school_ids=[ObjectId(sid) for sid in extra.get("school_holding",{}).get("school_ids")] if validated_data.get("holding_id") else [ObjectId(validated_data.get("school_id"))],
            prefix=validated_data.get("prefix"),
            name=name,
            account_no=validated_data.get("account_no"),
            account_name=validated_data.get("account_name"),
            purpose=validated_data.get("purpose"),
            fee=validated_data.get("fee"),
            partner_id=validated_data.get("partner_id"),
            client_id=validated_data.get("client_id"),
            client_secret=validated_data.get("client_secret"),
            key=validated_data.get("key"),
            is_school=True if validated_data.get("school_id") else False,
            is_holding=True if validated_data.get("holding_id") else False,
            is_active=True
        )
        SecurityValidator.validate_data(new_va_config_data)
        result = model.insert_one(new_va_config_data, user)
        if validated_data.get("holding_id"):
            update_data = []
            for sid in extra.get("school_holding",{}).get("school_ids"):
                update_data.append({
                    "_id": ObjectId(sid),
                    "add_to_set_data": {"config_va_ids": [ObjectId(new_va_config_data._id)]}
                })
            SchoolSchool.update_many_different_data(update_data)
        elif validated_data.get("school_id"):
            SchoolSchool().update_one(
                {"_id": ObjectId(validated_data.get("school_id"))},
                add_to_set_data={"config_va_ids": ObjectId(new_va_config_data._id)}
            )
        
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def list(
        model: BaseModel, query_params, params_validation, user, headers_dict=None
    ):
        result = model.aggregate(
            add_metadata=True,
            query_params=query_params,
            params_validation=params_validation,
            fields=query_params.get("fields"),
            exclude=query_params.get("exclude"),
            lookup=["bank", "vendor", "coa", "holding", "school", "schools"]
        )
        return result

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from utils.id_util import IDUtil
        school_ids = old_data.get("school_ids")
        if old_data.get("holding_id"):
            holding = SchoolHolding().find_one({"_id": ObjectId(old_data.get("holding_id"))})
            if holding:
                school_ids = holding.get("school_ids")
        name = f"{extra.get('res_bank',{}).get('short_name')} {validated_data.get('account_no')} An. {validated_data.get('account_name')}{validated_data.get('purpose')}"
        validated_data.update({"school_ids": school_ids, "name": name})
        _id = IDUtil.parse(_id, model.type_id)
        model.update_one({"_id": _id}, update_data=validated_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
    
    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        from utils.id_util import IDUtil

        _id = IDUtil.parse(_id, model.type_id)
        model.soft_delete({"_id": _id}, old_data, user=user)
        
        update_data = []
        for i in old_data.get("school_ids"):
            update_data.append({
                "_id": ObjectId(i),
                "pull_data": {"config_va_ids": [ObjectId(_id)]}
            })
        SchoolSchool().update_many_different_data(update_data)
        
        return {}