from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.mutabaah_practice_type_day import MutabaahPracticeTypeDay, MutabaahPracticeTypeDayData
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        existing_data = MutabaahPracticeTypeDay().find_one({
            "type_id":ObjectId(value.get("type_id")),
            "name":value.get("name")
        })
        if existing_data:
            raise ValidationError(f"The name '{value.get('name')}' for '{_extra.get('mutabaah_practice_type').get('name')}' type already exists.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_type_day_data = MutabaahPracticeTypeDayData(
            school_id=extra.get("mutabaah_practice_type").get("school_id"),
            type_id=validated_data.get("type_id"),
            name=validated_data.get("name"),
        )
        SecurityValidator.validate_data(new_type_day_data)
        result = model.insert_one(new_type_day_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        from models.mutabaah_practice_type import MutabaahPracticeType
        existing_data = MutabaahPracticeTypeDay().find({
            "type_id":old_data.get("type_id"),
            "name":{"$ne":old_data.get("name")}
        })
        if existing_data:
            existing_name = [i.get("name") for i in existing_data]
            if value.get("name") in existing_name:
                type_data = MutabaahPracticeType().find_one({"_id":old_data.get("type_id")})
                raise ValidationError(f"The name '{value.get('name')}' for '{type_data.get('name')}' type already exists.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

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
            lookup=["type"]
        )
        return result