from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.tap_type import TapType, TapTypeData
from models.tap_activity import TapActivity
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        existing_code = TapType().find_one({
            "code":value.get("code"),
            "activity_id":ObjectId(value.get("activity_id")),
        })
        if existing_code:
            raise ValidationError(f"Code '{value.get('code')}' already exists.")

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_type_data = TapTypeData(
            activity_id=ObjectId(validated_data.get("activity_id")),
            code=validated_data.get("code"),
            allow_context=validated_data.get("allow_context"),
            for_teacher=validated_data.get("for_teacher"),
            for_student=validated_data.get("for_student"),
        )
        SecurityValidator.validate_data(new_type_data)
        result = model.insert_one(new_type_data, user)
        TapActivity().update_one(
            {"_id":ObjectId(validated_data.get("activity_id"))},
            add_to_set_data={"type_ids":[new_type_data._id]}
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
            lookup=["activity"]
        )
        return result
    

    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        TapActivity().update_one(
            {"_id":ObjectId(old_data.get("activity_id"))},
            pull_data={"type_ids":[ObjectId(_id)]}
        )
        return {}
