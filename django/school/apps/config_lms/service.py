from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId
from constants.params_validation_type import ParamsValidationType


class MainService(BaseService):
    
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
            lookup=["exam_types","config_report"]
        )
        result["data"] = result.get("data")[0]
        return result
    
    
    @staticmethod
    def retrieve(
        model: BaseModel,
        _id,
        user,
        headers_dict=None,
        query_params={},
        params_validation={},
    ):
        result = model.aggregate(
            query_params={**query_params, "_id": ObjectId(_id)},
            params_validation={
                **params_validation,
                "_id": ParamsValidationType.OBJECT_ID,
            },
            lookup=["exam_types","config_report"]
        )
        return result[0]
    

    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        for k_extra,v_extra in _extra.items():
            if type(v_extra) == dict:
                for k,v in v_extra.items():
                    if k == "school_id":
                        if ObjectId(v) != old_data.get("school_id"):
                            raise ValidationError(f"Invalid {k_extra}_id. ID {v_extra.get('_id')} does not belong to that school.")
            if type(v_extra) == list:
                for item in v_extra:
                    for k,v in item.items():
                        if k == "school_id":
                            if ObjectId(v) != old_data.get("school_id"):
                                raise ValidationError(f"Invalid {k_extra}_id. ID {item.get('_id')} does not belong to that school.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}



    @staticmethod
    def me(
        model: BaseModel, query_params, params_validation, user, headers_dict=None
    ):
        result = model.aggregate(
            add_metadata=True,
            query_params=query_params,
            params_validation=params_validation,
            fields=query_params.get("fields"),
            exclude=query_params.get("exclude"),
            lookup=["exam_types","config_report"]
        )
        result["data"] = result.get("data")[0]
        return result
    

    @staticmethod
    def validate_update_me(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        for k_extra,v_extra in _extra.items():
            if type(v_extra) == dict:
                for k,v in v_extra.items():
                    if k == "school_id":
                        if v != user.school_id:
                            raise ValidationError(f"Invalid {k_extra}_id. ID {v_extra.get('_id')} does not belong to that school.")
            if type(v_extra) == list:
                for item in v_extra:
                    for k,v in item.items():
                        if k == "school_id":
                            if v != user.school_id:
                                raise ValidationError(f"Invalid {k_extra}_id. ID {item.get('_id')} does not belong to that school.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}
    

    @staticmethod
    def update_me(model: BaseModel, validated_data, extra, user, headers_dict=None):
        model.update_one({"school_id": ObjectId(user.school_id)}, update_data=validated_data, user=user)
        return {}
    