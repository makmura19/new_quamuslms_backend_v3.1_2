from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId
from models.psb_invoice import PsbInvoice, PsbInvoiceData
from models.psb_psb import PsbPsb


class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        existing = PsbInvoice().find_one({
            "holding_id": ObjectId(value.get("holding_id")) if value.get("holding_id") else None,
            "school_id": ObjectId(value.get("school_id")) if value.get("school_id") else None,
            "psb_id": ObjectId(value.get("psb_id")),
            "invoice_type_id": ObjectId( value.get("invoice_type_id"))
        })
        if existing:
            raise ValidationError("Data sudah digunakan.")
        
        if value.get("holding_id"):
            school_ids = _extra.get("school_holding",{}).get("school_ids")
            if _extra.get("psb_psb",{}).get("holding_id") != value.get("holding_id"):
                raise ValidationError("Data yayasan dan PSB tidak sesuai.")
            if _extra.get("psb_psb",{}).get("school_id") not in school_ids:
                raise ValidationError("Data sekolah dan PSB tidak sesuai.")
        elif value.get("school_id"):
            if _extra.get("psb_psb",{}).get("school_id") != value.get("school_id"):
                raise ValidationError("Data sekolah dan PSB tidak sesuai.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        
        new_invoice_data = PsbInvoiceData(
            holding_id=ObjectId(validated_data.get("holding_id")) if validated_data.get("holding_id") else None,
            school_id=ObjectId(validated_data.get("school_id")) if validated_data.get("holding_id") else None,
            invoice_type_id=ObjectId(validated_data.get("invoice_type_id")),
            month=validated_data.get("month", []),
            semester=validated_data.get("semester", []),
            psb_id=ObjectId(validated_data.get("psb_id")),
        )
        SecurityValidator.validate_data(new_invoice_data)
        result = model.insert_one(new_invoice_data, user)
        PsbPsb().update_one(
            {"_id": ObjectId(validated_data.get("psb_id"))},
            add_to_set_data={"invoice_ids": [ObjectId(new_invoice_data._id)]}
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
            lookup=["holding", "school", "psb", "invoice_type"]
        )
        return result
    
    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        from utils.id_util import IDUtil

        _id = IDUtil.parse(_id, model.type_id)
        model.soft_delete({"_id": _id}, old_data, user=user)
        PsbPsb().update_one(
            {"_id": ObjectId(old_data.get("psb_id"))},
            pull_data={"invoice_ids": [ObjectId(_id)]})
        
        return {}

