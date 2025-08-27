from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.school_dormitory import SchoolDormitoryData
from models.school_holding import SchoolHolding
from models.school_school import SchoolSchool
from bson import ObjectId


class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        if value.get("school_id") and value.get("holding_id"):
            raise ValidationError("Invalid, fill one of school_id or holding_id")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_dormitory_data = SchoolDormitoryData(
            holding_id=ObjectId(validated_data.get("holding_id")),
            school_id=ObjectId(validated_data.get("holding_id")),
            name=validated_data.get("name"),
            gender=validated_data.get("gender"),
            capacity=validated_data.get("capacity"),
            is_active=validated_data.get("is_active"),
        )
        SecurityValidator.validate_data(new_dormitory_data)
        result = model.insert_one(new_dormitory_data, user=user)
        if validated_data.get("holding_id"):
            SchoolHolding().update_one(
                {"_id": ObjectId(validated_data.get("holding_id"))},
                add_to_set_data={"dormitory_ids": [new_dormitory_data._id]},
            )
        if validated_data.get("school_id"):
            SchoolSchool().update_one(
                {"_id": ObjectId(validated_data.get("school_id"))},
                add_to_set_data={"dormitory_ids": [new_dormitory_data._id]},
            )
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        school_data = SchoolSchool().find_one(
            {"_id": ObjectId(old_data.get("school_id"))}
        )
        holding_id = school_data.get("holding_id")
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        if holding_id is not None:
            SchoolHolding().update_one(
                {"_id": ObjectId(holding_id)},
                pull_data={"dormitory_ids": [ObjectId(_id)]},
                user=user,
            )
        if old_data.get("school_id") is not None:
            SchoolSchool().update_one(
                {"_id": ObjectId(old_data.get("school_id"))},
                pull_data={"dormitory_ids": [ObjectId(_id)]},
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
            lookup=["holding","school","schools","staffs","rooms"]
        )
        return result
