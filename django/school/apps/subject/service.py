from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.school_subject import SchoolSubjectData
from models.school_school import SchoolSchool
from models.edu_subject import EduSubject
from bson import ObjectId


class MainService(BaseService):

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        sequence = model.count_data({"school_id":ObjectId(validated_data.get("school_id"))}) + 1
        new_subject_data = SchoolSubjectData(
            school_id=ObjectId(validated_data.get("school_id")),
            name=validated_data.get("name"),
            short_name=validated_data.get("short_name"),
            treshold=validated_data.get("treshold"),
            sequence=sequence,
            is_active=validated_data.get("is_active"),
        )
        SecurityValidator.validate_data(new_subject_data)
        result = model.insert_one(new_subject_data, user)
        SchoolSchool().update_one(
            {"_id": ObjectId(validated_data.get("school_id"))},
            add_to_set_data={"subject_ids":new_subject_data._id},
            user=user
        )
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }
    

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        update_data = {
            "name":validated_data.get("name"),
            "short_name":validated_data.get("short_name"),
            "treshold":validated_data.get("treshold"),
            "is_active":validated_data.get("is_active"),
        }
        model.update_one({"_id": ObjectId(_id)}, update_data=update_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
    

    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        SchoolSchool().update_one(
            {"_id": ObjectId(old_data.get("school_id"))},
            pull_data={"subject_ids":[ObjectId(_id)]},
            user=user
        )
        return {}
    
    
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
            lookup=["school","subject","levels"]
        )
        return result
    

    @staticmethod
    def upload_img(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from utils.file_storage_util import FileStorageUtil
        from helpers.user_service import UserService

        url = FileStorageUtil.upload_aws(validated_data.get("file"), "school_subject_img")
        if not url:
            raise ValidationError("Failed to upload image.")
        update_data = {"image": url[0]}
        model.update_one({"_id": ObjectId(_id)}, update_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
    

    @staticmethod
    def validate_sequence(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        for subject_data in _extra.get("school_subject"):
            if subject_data.get("school_id") != value.get("school_id"):
                raise ValidationError(f"Invalid subject_id ({subject_data.get('_id')})")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}


    @staticmethod
    def sequence(model: BaseModel, validated_data, extra, user, headers_dict=None):
        model.update_sequence(validated_data.get("_ids"))
        return {
            "message": None,
        }
