from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId
from constants.params_validation_type import ParamsValidationType


class MainService(BaseService):
    
    @staticmethod
    def retrieve(
        model: BaseModel,
        _id,
        user,
        headers_dict=None,
        query_params={},
        params_validation={},
    ):
        from models.lms_report_type import LmsReportType

        result = model.aggregate(
            query_params={**query_params, "_id": ObjectId(_id)},
            params_validation={
                **params_validation,
                "_id": ParamsValidationType.OBJECT_ID,
            },
            lookup=["exam_types","config_report"]
        )[0]
        report_type_id = ObjectId(result.get("config_report_info").get("type_id"))
        report_type_data = LmsReportType().find_one({"_id":report_type_id})
        result["config_report_info"].update({"type_name":report_type_data.get("name")})
        return result
    

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
    
