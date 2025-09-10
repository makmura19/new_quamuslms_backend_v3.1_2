from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId
from models.psb_logistic import PsbLogistic, PsbLogisticData
from models.psb_psb import PsbPsb


class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        existing = PsbLogistic().find_one({
            "holding_id": ObjectId(value.get("holding_id")) if value.get("holding_id") else None,
            "school_id": ObjectId(value.get("school_id")) if value.get("school_id") else None,
            "psb_id": ObjectId(value.get("psb_id")),
            "name": value.get("name")
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
        
        target_school_ids = []
        if validated_data.get("holding_id"):
            target_school_ids = [ObjectId(i) for i in extra.get("school_holding",{}).get("school_ids")]
        elif validated_data.get("school_id"):
            target_school_ids = [ObjectId(validated_data.get("school_id"))]
            
        new_logistic_data = PsbLogisticData(
            holding_id=ObjectId(validated_data.get("holding_id")) if validated_data.get("holding_id") else None,
            school_id=ObjectId(validated_data.get("school_id")) if validated_data.get("school_id") else None,
            psb_id=ObjectId(validated_data.get("psb_id")),
            target_school_ids=target_school_ids,
            gender=validated_data.get("gender"),
            boarding=validated_data.get("boarding"),
            name=validated_data.get("name"),
            qty=validated_data.get("qty"),
            qty_unit=validated_data.get("qty_unit"),
        )
        SecurityValidator.validate_data(new_logistic_data)
        result = model.insert_one(new_logistic_data, user)
        PsbPsb().update_one(
            {"_id": ObjectId(validated_data.get("psb_id"))},
            add_to_set_data={"logistic_ids": [ObjectId(new_logistic_data._id)]}
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
            lookup=["holding", "school", "psb", "target_schools"]
        )
        return result
    
    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        from utils.id_util import IDUtil

        _id = IDUtil.parse(_id, model.type_id)
        model.soft_delete({"_id": _id}, old_data, user=user)
        PsbPsb().update_one(
            {"_id": ObjectId(old_data.get("psb_id"))},
            pull_data={"logistic_ids": [ObjectId(_id)]})
        
        return {}