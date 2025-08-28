from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.res_bank import ResBank, ResBankData
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        
        exists_bank_data = ResBank().find()
        exists_names = [i.get("name") for i in exists_bank_data]
        exists_short_names = [i.get("short_name") for i in exists_bank_data]
        if value.get("name") in exists_names:
            raise ValidationError(f"The name '{value.get('name')}' already exists.")
        if value.get("short_name") in exists_short_names:
            raise ValidationError(f"The short name '{value.get('short_name')}' already exists.")

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        
        new_bank_data = ResBankData(
            name=validated_data.get("name"),
            short_name=validated_data.get("short_name"),
            is_active=validated_data.get("is_active"),
        )
        SecurityValidator.validate_data(new_bank_data)
        result = model.insert_one(new_bank_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }


    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        
        exists_bank_data = ResBank().find({"_id":{"$ne":old_data.get("_id")}})
        exists_names = [i.get("name") for i in exists_bank_data]
        exists_short_names = [i.get("short_name") for i in exists_bank_data]
        if value.get("name") in exists_names:
            raise ValidationError(f"The name '{value.get('name')}' already exists.")
        if value.get("short_name") in exists_short_names:
            raise ValidationError(f"The short name '{value.get('short_name')}' already exists.")

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}


    @staticmethod
    def upload_image(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from utils.file_storage_util import FileStorageUtil

        url = FileStorageUtil.upload_aws(validated_data.get("file"), "bank_image")
        if not url:
            raise ValidationError("Failed to upload image.")
        update_data = {"image": url[0]}
        model.update_one({"_id": ObjectId(_id)}, update_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
