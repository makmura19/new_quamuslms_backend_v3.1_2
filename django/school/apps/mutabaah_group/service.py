from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.mutabaah_practice_type import MutabaahPracticeType
from models.mutabaah_practice_rubric import MutabaahPracticeRubric
from models.mutabaah_group import MutabaahGroupData
from bson import ObjectId
from utils.dict_util import DictUtil
from utils.array_util import ArrayUtil


class MainService(BaseService):

    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        if _extra.get("mutabaah_practice_type"):
            for practice_data in _extra.get("mutabaah_practice_type"):
                if practice_data.get("school_id") != value.get("school_id"):
                    raise ValidationError(f"Invalid practice_id. ID {practice_data.get('_id')} does not belong to this school.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    
    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        sequence = model.count_data({"school_id":ObjectId(validated_data.get("school_id"))}) + 1
        new_group_data = MutabaahGroupData(
            school_id=ObjectId(validated_data.get("school_id")),
            name=validated_data.get("name"),
            parent_id=None,
            child_ids=[],
            sequence=sequence,
            is_parent=True,
            is_child=False,
            practice_ids=[ObjectId(i) for i in validated_data.get("practice_ids", [])],
            rubric_id=ObjectId(validated_data.get("rubric_id")) if validated_data.get("rubric_id") else None,
        )
        SecurityValidator.validate_data(new_group_data)
        result = model.insert_one(new_group_data, user)
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
            lookup=["parent","children","practice","rubric"]
        )
        return result
    

    @staticmethod
    def validate_sequence(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        for group_data in _extra.get("mutabaah_group"):
            if group_data.get("school_id") != value.get("school_id"):
                raise ValidationError(f"Invalid mutabaah_group_id. ID {group_data.get('_id')} does not belong to this school.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}


    @staticmethod
    def sequence(model: BaseModel, validated_data, extra, user, headers_dict=None):
        model.update_sequence(validated_data.get("_ids"))
        return {
            "message": None,
        }
