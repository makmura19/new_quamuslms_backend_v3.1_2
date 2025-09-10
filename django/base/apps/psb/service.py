from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.psb_psb import PsbPsb, PsbPsbData
from models.psb_document import PsbDocument
from models.psb_invoice import PsbInvoice
from models.psb_logistic import PsbLogistic
from models.psb_program import PsbProgram
from bson import ObjectId

class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
                
        existing = PsbPsb().find_one({
            "holding_id": ObjectId(value.get("holding_id")) if value.get("holding_id") else None,
            "school_id": ObjectId(value.get("school_id")) if value.get("school_id") else None,
            "name": value.get("name")
        })
        if existing:
            raise ValidationError(f"Data PSB dengan nama {value.get('name')} sudah ada.")
        
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_psb_data = PsbPsbData(
            holding_id=ObjectId(validated_data.get("holding_id")) if validated_data.get("holding_id") else None,
            school_id=ObjectId(validated_data.get("school_id")) if validated_data.get("school_id") else None,
            staff_ids=[ObjectId(sid) for sid in validated_data.get("staff_ids",[])],
            va_config_id=ObjectId(validated_data.get("va_config_id")),
            name=validated_data.get("name"),
            document_ids=[],
            invoice_ids=[],
            logistic_ids=[],
            fee=validated_data.get("fee"),
            is_school=True if validated_data.get("school_id") else False,
            is_holding=True if validated_data.get("holding_id") else False,
            is_active=True
        )
        SecurityValidator.validate_data(new_psb_data)
        result = model.insert_one(new_psb_data, user)
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
            lookup=["holding", "school", "staff", "va_config", "document", "invoice", "logistic"]
        )
        return result
    
    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        from utils.id_util import IDUtil
        
        PsbDocument().soft_delete_many({"psb_id": ObjectId(_id)})
        PsbInvoice().soft_delete_many({"psb_id": ObjectId(_id)})
        PsbLogistic().soft_delete_many({"psb_id": ObjectId(_id)})
        PsbProgram().soft_delete_many({"psb_id": ObjectId(_id)})
        
        _id = IDUtil.parse(_id, model.type_id)
        model.soft_delete({"_id": _id}, old_data, user=user)
        
        return {}