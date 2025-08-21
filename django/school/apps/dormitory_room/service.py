from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.school_dormitory_room import SchoolDormitoryRoomData
from models.school_dormitory import SchoolDormitory
from bson import ObjectId


class MainService(BaseService):

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_dormitory_room_data = SchoolDormitoryRoomData(
            **validated_data,
            holding_id=extra.get("school_dormitory").get("holding_id"),
            school_id=extra.get("school_dormitory").get("school_id")
        )
        SecurityValidator.validate_data(new_dormitory_room_data)
        result = model.insert_one(new_dormitory_room_data, user)
        SchoolDormitory().update_one(
            {"_id": ObjectId(validated_data.get("dormitory_id"))},
            add_to_set_data={"room_ids": new_dormitory_room_data._id},
            user=user,
        )
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        SchoolDormitory().update_one(
            {"_id": ObjectId(old_data.get("dormitory_id"))},
            pull_data={"room_ids": [ObjectId(_id)]},
            user=user,
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
            lookup=["dormitory"],
        )
        return result
