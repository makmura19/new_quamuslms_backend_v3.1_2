from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from models.edu_stage import EduStageData
from models.edu_stage_group import EduStageGroup
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId


class MainService(BaseService):
    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_stage_data = EduStageData(
            group_id=ObjectId(validated_data.get("group_id")),
            name=validated_data.get("name"),
            short_name=validated_data.get("short_name"),
            origin=validated_data.get("origin"),
        )
        SecurityValidator.validate_data(new_stage_data)
        result = model.insert_one(new_stage_data)
        EduStageGroup().update_one(
            {"_id": ObjectId(validated_data.get("group_id"))},
            add_to_set_data={"stage_ids": [new_stage_data._id]},
        )
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        EduStageGroup().update_one(
            {"_id": old_data.get("group_id")}, pull_data={"stage_ids": [ObjectId(_id)]}
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
            lookup=["group"],
        )
        return result
