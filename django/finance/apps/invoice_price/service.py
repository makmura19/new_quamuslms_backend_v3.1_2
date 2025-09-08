from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.finance_invoice_type import FinanceInvoiceType
from models.finance_invoice_price_variant import FinanceInvoicePriceVariant
from models.finance_invoice_price import FinanceInvoicePriceData
from utils.array_util import ArrayUtil
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        if not ArrayUtil.is_unique(value.get("invoice_type"), key="_id"):
            raise ValidationError("invoice_type tidak valid")
        invoice_type_ids = [
            ObjectId(item.get("_id")) for item in value.get("invoice_type")
        ]
        finance_invoice_type_data = FinanceInvoiceType().find({
            "school_id": ObjectId(value.get("school_id"))
        })
        finance_invoice_type_ids = [
            ObjectId(item.get("_id")) for item in finance_invoice_type_data
        ]
        if set(finance_invoice_type_ids) != set(invoice_type_ids):
            raise ValidationError("invoice_type tidak valid")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        old_data = model.find(
            {
                "school_id": ObjectId(validated_data.get("school_id")),
                "level_id": ObjectId(validated_data.get("level_id")),
            },
        )
        old_data_ids = []
        old_variant_ids = []
        for item in old_data:
            old_data_ids.append(ObjectId(item.get("_id")))
            old_variant_ids.extend([ObjectId(i) for i in item.get("variant_ids")])
            # print()
            FinanceInvoiceType().update_one(
                {"_id":ObjectId(item.get("type_id"))},
                pull_data={"price_ids":[ObjectId(item.get("_id"))]},
                user=user
            )
        if old_data_ids:
            model.update_many({"_id":{"$in":old_data_ids}},{"is_active":False})
        if old_variant_ids:
            FinanceInvoicePriceVariant().update_many({"_id":{"$in":old_variant_ids}},{"is_active":False})

        input_data = []
        update_data = []
        update_type_data = []
        update_variant_ids = []
        for item in validated_data.get("invoice_type"):
            if item.get("is_exists"):
                existing_invoice_price_data = model.find_one({
                    "school_id": ObjectId(validated_data.get("school_id")),
                    "type_id": ObjectId(item.get("_id")),
                    "level_id": ObjectId(validated_data.get("level_id")),
                })
                price_id = None
                if not existing_invoice_price_data:
                    new_invoice_price_data = FinanceInvoicePriceData(
                        school_id=ObjectId(validated_data.get("school_id")),
                        type_id=ObjectId(item.get("_id")),
                        level_id=ObjectId(validated_data.get("level_id")),
                        amount=item.get("amount"),
                        is_active=True,
                    )
                    input_data.append(new_invoice_price_data)
                    price_id = new_invoice_price_data._id
                else:
                    price_id = ObjectId(existing_invoice_price_data.get("_id"))
                    update_data.append({
                        "_id": price_id,
                        "set_data": {"amount": item.get("amount"), "is_active":True},
                    })
                    update_variant_ids.append([ObjectId(i) for i in existing_invoice_price_data.get("variant_ids")])
                update_type_data.append({
                    "_id": ObjectId(item.get("_id")),
                    "add_to_set_data": {"price_ids": [price_id]},
                })

        if input_data:
            SecurityValidator.validate_data(input_data)
            model.insert_many(input_data)
        if update_data:
            model.update_many_different_data(update_data)
            FinanceInvoicePriceVariant().update_many({"_id":{"$in":update_variant_ids}},{"is_active":True})
        FinanceInvoiceType().update_many_different_data(update_type_data)
            
        return {
            "data": {},
            "message": None,
        }


    @staticmethod
    def list(
        model: BaseModel, query_params, params_validation, user, headers_dict=None
    ):
        finance_invoice_type_data = FinanceInvoiceType().find(
            {"school_id": ObjectId(query_params.get("school_id")), "is_active": True},
            query_params=({"sort": "type,name"}),
        )

        invoice_price_data = model.aggregate(
            query_params=query_params,
            params_validation=params_validation,
            fields=query_params.get("fields"),
            exclude=query_params.get("exclude"),
            lookup=["variants"],
        )

        invoice_price_data = {
            ObjectId(item.get("type_id")): item for item in invoice_price_data
        }

        data = [
            {
                **item,
                "is_exists": True if invoice_price_data.get(ObjectId(item.get("_id"))) and  invoice_price_data.get(ObjectId(item.get("_id"))).get("is_active") == True else False,
                "price_id": (
                    invoice_price_data.get(ObjectId(item.get("_id"))).get("_id")
                    if invoice_price_data.get(ObjectId(item.get("_id")))
                    else None
                ),
                "amount": (
                    invoice_price_data.get(ObjectId(item.get("_id"))).get("amount")
                    if invoice_price_data.get(ObjectId(item.get("_id")))
                    else 0
                ),
                "variant_ids": (
                    invoice_price_data.get(ObjectId(item.get("_id"))).get("variant_ids")
                    if invoice_price_data.get(ObjectId(item.get("_id")))
                    else []
                ),
                "variants_info": (
                    invoice_price_data.get(ObjectId(item.get("_id"))).get("variants_info")
                    if invoice_price_data.get(ObjectId(item.get("_id")))
                    else []
                ),
            }
            for item in finance_invoice_type_data
        ]

        return {"data": data}