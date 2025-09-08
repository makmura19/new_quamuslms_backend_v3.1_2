from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.finance_invoice_price import FinanceInvoicePrice
from models.finance_invoice_price_variant import FinanceInvoicePriceVariantData
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        from models.school_school import SchoolSchool

        school_id = ObjectId(_extra.get("finance_invoice_price").get("school_id"))
        school_data = SchoolSchool().find_one({"_id":school_id})
        ref_list = []
        for item in value.get("variant"):
            if item.get("degree_id"):
                if item.get("degree_id") not in school_data.get("degree_ids"):
                    raise ValidationError(f"Invalid degree_id ({item.get('degree_id')}).")
            if item.get("major_id"):
                if item.get("major_id") not in school_data.get("major_ids"):
                    raise ValidationError(f"Invalid major_id ({item.get('major_id')}).")
            if item.get("program_id"):
                if item.get("program_id") not in school_data.get("program_ids"):
                    raise ValidationError(f"Invalid program_id ({item.get('program_id')}).")
            data_to_compare = {
                "gender": item.get("gender"),
                "is_boarding": item.get("is_boarding"),
                "is_alumni": item.get("is_alumni"),
                "degree_id": item.get("degree_id"),
                "major_id": item.get("major_id"),
                "program_id": item.get("program_id"),
            }
            if data_to_compare in ref_list:
                raise ValidationError(f"Variants may not be duplicated.")
            else:
                ref_list.append(data_to_compare)

        extra = {"school_data":school_data}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        price_id = ObjectId(validated_data.get("invoice_price_id"))
        model.update_many({"price_id":price_id},{"is_active":False})

        input_data = []
        variant_ids = []
        update_data = []
        for item in validated_data.get("variant"):
            existing_variant_data = model.find_one({
                "price_id": price_id,
                "gender": item.get("gender"),
                "is_boarding": item.get("is_boarding"),
                "is_alumni": item.get("is_alumni"),
                "degree_id": ObjectId(item.get("degree_id")) if item.get("degree_id") else None,
                "major_id": ObjectId(item.get("major_id")) if item.get("major_id") else None,
                "program_id": ObjectId(item.get("program_id")) if item.get("program_id") else None,
            })
            if not existing_variant_data:
                new_variant_data = FinanceInvoicePriceVariantData(
                    school_id=ObjectId(extra.get("school_data").get("_id")),
                    price_id=price_id,
                    type_id=ObjectId(extra.get("finance_invoice_price").get("type_id")),
                    gender=item.get("gender"),
                    is_boarding=item.get("is_boarding"),
                    is_alumni=item.get("is_alumni"),
                    degree_id=ObjectId(item.get("degree_id")) if item.get("degree_id") else None,
                    major_id=ObjectId(item.get("major_id")) if item.get("major_id") else None,
                    program_id=ObjectId(item.get("program_id")) if item.get("program_id") else None,
                    amount=item.get("amount"),
                    is_active=True,
                )
                input_data.append(new_variant_data)
                variant_ids.append(new_variant_data._id)
            else:
                variant_id = ObjectId(existing_variant_data.get("_id"))
                variant_ids.append(variant_id)
                update_data.append({
                    "_id": variant_id,
                    "set_data": {"amount": item.get("amount"), "is_active":True},
                })

        SecurityValidator.validate_data(input_data)
        if input_data:
            SecurityValidator.validate_data(input_data)
            model.insert_many(input_data)
        if update_data:
            model.update_many_different_data(update_data)
        FinanceInvoicePrice().update_one(
            {"_id":price_id},
            {"variant_ids":variant_ids}
        )
        return {
            "data": {},
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
            lookup=["degree", "major", "program"]
        )
        return result