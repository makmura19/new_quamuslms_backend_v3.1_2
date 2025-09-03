from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.tap_activity import TapActivity, TapActivityData
from models.tap_type import TapType
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        existing_code = TapActivity().find_one({"code":value.get("code")})
        if existing_code:
            raise ValidationError(f"Code '{value.get('code')}' already exists.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_activity_data = TapActivityData(
            code=validated_data.get("code"),
            name=validated_data.get("name"),
            description=validated_data.get("description"),
            required_tap_count=validated_data.get("required_tap_count"),
            is_attendance=validated_data.get("is_attendance"),
        )
        SecurityValidator.validate_data(new_activity_data)
        result = model.insert_one(new_activity_data, user)
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
            lookup=["types"]
        )
        return result
    

    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        TapType().soft_delete_many({"_id":{"$in":old_data.get("type_ids")}})
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        return {}
