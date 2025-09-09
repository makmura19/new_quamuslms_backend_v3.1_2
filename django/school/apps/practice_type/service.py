from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.mutabaah_practice_type import MutabaahPracticeTypeData
from utils.array_util import ArrayUtil
from utils.dict_util import DictUtil
from bson import ObjectId

class MainService(BaseService):
    
    @staticmethod
    def validate_create_update(value):
        if not ArrayUtil.is_unique(value.get("days_of_week")):
            raise ValidationError("Days_of_week values cannot be the same.")
        if value.get("type") == "boolean" and value.get("unit") != None and value.get("options") != []:
            raise ValidationError("For boolean type, unit and option must be empty.")
        if value.get("type") == "quantitative" and value.get("unit") == None:
            raise ValidationError("For quantitative type, unit must be filled.")
        if value.get("type") == "options" and (not value.get("options") or len(value.get("options")) == 0):
            raise ValidationError("For quantitative type, options must be filled.")
        if value.get("type") == "time" and (not value.get("interval") or not value.get("penalty_per_interval")):
            raise ValidationError(f"For time type, interval and penalty_per_interval must be filled.")


    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        MainService.validate_create_update(value)
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}
    

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        sequence = model.count_data({"school_id":validated_data.get("school_id")}) + 1
        new_practice_type_data = MutabaahPracticeTypeData(
            school_id=ObjectId(validated_data.get("school_id")),
            name=validated_data.get("name"),
            description=validated_data.get("description"),
            type=validated_data.get("type"),
            unit=validated_data.get("unit"),
            period=validated_data.get("period"),
            interval=validated_data.get("interval"),
            penalty_per_interval=validated_data.get("penalty_per_interval"),
            options=validated_data.get("options"),
            days_of_week=validated_data.get("days_of_week"),
            gender=validated_data.get("gender"),
            sequence=sequence,
            mandatory_type=validated_data.get("mandatory_type"),
            submitted_by=validated_data.get("submitted_by"),
            rubric_id=ObjectId(validated_data.get("rubric_id")) if validated_data.get("rubric_id") else None,
            use_timeconfig=True if validated_data.get("type") == "time" else False,
            use_penalty=True if validated_data.get("type") == "time" else False,
            is_mandatory_shalat=validated_data.get("is_mandatory_shalat"),
        )
        SecurityValidator.validate_data(new_practice_type_data)
        result = model.insert_one(new_practice_type_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }
    

    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        MainService.validate_create_update(value)
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}


    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        update_practice_type_data = {
            "name":validated_data.get("name"),
            "description":validated_data.get("description"),
            "type":validated_data.get("type"),
            "unit":validated_data.get("unit"),
            "period":validated_data.get("period"),
            "interval":validated_data.get("interval"),
            "penalty_per_interval":validated_data.get("penalty_per_interval"),
            "options":validated_data.get("options"),
            "days_of_week":validated_data.get("days_of_week"),
            "gender":validated_data.get("gender"),
            "mandatory_type":validated_data.get("mandatory_type"),
            "submitted_by":validated_data.get("submitted_by"),
            "rubric_id":ObjectId(validated_data.get("rubric_id")) if validated_data.get("rubric_id") else None,
            "use_timeconfig":True if validated_data.get("type") == "time" else False,
            "use_penalty":True if validated_data.get("type") == "time" else False,
            "is_mandatory_shalat":validated_data.get("is_mandatory_shalat"),
        }
        model.update_one({"_id": ObjectId(_id)}, update_data=update_practice_type_data, user=user)
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
            lookup=["school","rubric","day_count"]
        )
        return result