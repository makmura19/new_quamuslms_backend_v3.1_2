from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.finance_invoice_type import FinanceInvoiceTypeData
from models.account_account import AccountAccount
from models.finance_invoice_price import FinanceInvoicePrice
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        school_id = ObjectId(validated_data.get("school_id"))
        holding_id = ObjectId(extra.get("school_school").get("holding_id")) if extra.get("school_school").get("holding_id") else None

        income_coa_id = AccountAccount().create_account(
            "4100",
            holding_id,
            school_id,
            validated_data.get("name"),
            user=user,
        )
        payable_coa_id = AccountAccount().create_account(
            "1300",
            holding_id,
            school_id,
            validated_data.get("name"),
            user=user,
        )
        new_invoice_type_data = FinanceInvoiceTypeData(
            school_id=school_id,
            type=validated_data.get("type"),
            name=validated_data.get("name"),
            description=validated_data.get("description"),
            due_days=validated_data.get("due_days"),
            income_coa_id=income_coa_id,
            payable_coa_id=payable_coa_id,
            is_male=validated_data.get("is_male"),
            is_female=validated_data.get("is_female"),
            is_installment=validated_data.get("is_installment"),
            is_active=validated_data.get("is_active"),
        )
        SecurityValidator.validate_data(new_invoice_type_data)
        result = model.insert_one(new_invoice_type_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }
    

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        update_invoice_type_data = {
            "type":validated_data.get("type"),
            "name":validated_data.get("name"),
            "description":validated_data.get("description"),
            "due_days":validated_data.get("due_days"),
            "is_male":validated_data.get("is_male"),
            "is_female":validated_data.get("is_female"),
            "is_installment":validated_data.get("is_installment"),
            "is_active":validated_data.get("is_active"),
        }
        if old_data.get("name") != validated_data.get("name"):
            income_coa_data = AccountAccount().find_one({"_id":ObjectId(old_data.get("income_coa_id"))})
            income_coa_name = income_coa_data.get("name").replace(old_data.get("name"),validated_data.get("name"))
            payable_coa_data = AccountAccount().find_one({"_id":ObjectId(old_data.get("payable_coa_id"))})
            payable_coa_name = payable_coa_data.get("name").replace(old_data.get("name"),validated_data.get("name"))
            AccountAccount().update_many_different_data([
                {
                    "_id":ObjectId(old_data.get("income_coa_id")),
                    "set_data": {"name": income_coa_name},
                },
                {
                    "_id":ObjectId(old_data.get("payable_coa_id")),
                    "set_data": {"name": payable_coa_name},
                }
            ])

        model.update_one({"_id": ObjectId(_id)}, update_data=update_invoice_type_data, user=user)
        return {
            "data": {"id": str(_id)},
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
            lookup=["prices"]
        )
        return result


    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        income_coa_id = ObjectId(old_data.get("income_coa_id"))
        income_coa_data = AccountAccount().find_one({"_id":income_coa_id})
        income_coa_parent_id = ObjectId(income_coa_data.get("parent_id"))
        payable_coa_id = ObjectId(old_data.get("payable_coa_id"))
        payable_coa_data = AccountAccount().find_one({"_id":payable_coa_id})
        payable_coa_parent_id = ObjectId(payable_coa_data.get("parent_id"))
        price_ids = [ObjectId(i) for i in old_data.get("price_ids")]
            
        AccountAccount().update_one(
            {"_id":income_coa_parent_id},
            pull_data={"child_ids":[income_coa_id]}
        )
        AccountAccount().update_one(
            {"_id":payable_coa_parent_id},
            pull_data={"child_ids":[payable_coa_id]}
        )
        AccountAccount().soft_delete_many({"_id": {"$in":[income_coa_id,payable_coa_id]}})
        FinanceInvoicePrice().soft_delete_many({"_id": {"$in":price_ids}})
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        return {}

    
    @staticmethod
    def import_xlsx(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from utils.excel_util import ExcelUtils

        schema = {
            "NAMA": {"type": "string", "required": True},
            "TIPE": {
                "type": "enum",
                "choices": ["month", "semester", "year"],
                "required": True,
            },
            "JATUH TEMPO": {"type": "int", "required": True},
            "TARGET": {
                "type": "enum",
                "choices": ["all", "male", "female"],
                "required": True,
            },
            "DICICIL": {
                "type": "enum",
                "choices": ["0", "1"],
                "required": True,
            },
        }

        excel_data = ExcelUtils.read(validated_data.get("file"), schema=schema)
        if not excel_data:
            raise ValidationError("File tidak valid.")
        
        school_id = ObjectId(validated_data.get("school_id"))
        holding_id = ObjectId(extra.get("school_school").get("holding_id")) if extra.get("school_school").get("holding_id") else None

        input_data = []
        for i in excel_data:
            income_coa_id = AccountAccount().create_account(
                "4100",
                holding_id,
                school_id,
                i.get("NAMA"),
                user=user,
            )
            payable_coa_id = AccountAccount().create_account(
                "1300",
                holding_id,
                school_id,
                i.get("NAMA"),
                user=user,
            )
            new_invoice_type_data = FinanceInvoiceTypeData(
                school_id=school_id,
                type=i.get("TIPE"),
                name=i.get("NAMA"),
                description="",
                due_days=i.get("JATUH TEMPO"),
                income_coa_id=income_coa_id,
                payable_coa_id=payable_coa_id,
                is_male=i.get("TARGET") in ["male", "all"],
                is_female=i.get("TARGET") in ["female", "all"],
                is_installment=i.get("DICICIL") == "1",
                is_active=True
            )
            input_data.append(new_invoice_type_data)
        SecurityValidator.validate_data(input_data)
        model.insert_many(input_data)
        return {
            "data": {},
            "message": None,
        }