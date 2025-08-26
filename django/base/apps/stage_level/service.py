from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.edu_stage_group import EduStageGroup
from models.edu_stage_level import EduStageLevelData
from bson import ObjectId


class MainService(BaseService):

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        existing = model.find({})
        new_data = EduStageLevelData(
            degree_id=(
                ObjectId(validated_data.get("degree_id"))
                if validated_data.get("degree_id")
                else None
            ),
            group_id=ObjectId(validated_data.get("group_id")),
            name=validated_data.get("name"),
            sequence=len(existing) + 1,
            is_final=validated_data.get("is_final"),
            is_extension=validated_data.get("is_extension"),
        )

        SecurityValidator.validate_data(new_data)
        result = model.insert_one(new_data, user)
        level_data = model.find(
            {"group_id": ObjectId(validated_data.get("group_id"))},
            params_validation={"sort": "sequence"},
        )
        level_ids = [ObjectId(item.get("_id")) for item in level_data]
        EduStageGroup().update_one(
            {"_id": ObjectId(validated_data.get("group_id"))}, {"level_ids": level_ids}
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
            lookup=["degree", "group", "subjects"],
        )
        return result

    @staticmethod
    def validate_sequence(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        for i in _extra.get("edu_stage_level"):
            if ObjectId(i.get("group_id")) != ObjectId(value.get("group_id")):
                raise ValidationError("Invalid _ids")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def sequence(model: BaseModel, validated_data, extra, user, headers_dict=None):
        # print(validated_data)
        # print(extra)
        model.update_sequence(validated_data.get("_ids"))
        level_ids = [ObjectId(item) for item in validated_data.get("_ids")]
        EduStageGroup().update_one(
            {"_id": ObjectId(validated_data.get("group_id"))}, {"level_ids": level_ids}
        )

        return {
            "message": None,
        }
