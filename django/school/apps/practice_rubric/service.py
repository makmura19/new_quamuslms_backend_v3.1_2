from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.mutabaah_practice_rubric import MutabaahPracticeRubricData
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        sorted_list = sorted(value.get("list"), key=lambda x: x['lte'])
        is_correct_gap = all([(sorted_list[idx+1].get("gte") - i.get("lte")) == 1 for idx, i in enumerate(sorted_list) if idx < len(sorted_list)-1])
        if not is_correct_gap:
            raise ValidationError("Gap antara batas atas dan batas bawah skor harus 1.")
        

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_practice_rubric_data = MutabaahPracticeRubricData(
            school_id=ObjectId(validated_data.get("school_id")),
            level_id=ObjectId(validated_data.get("level_id")) if validated_data.get("level_id") else None,
            name=validated_data.get("name"),
            list=validated_data.get("list"),
            is_practice=validated_data.get("is_practice"),
            is_report=validated_data.get("is_report"),
            is_group=validated_data.get("is_group"),
            is_program=validated_data.get("is_program"),
            is_active=validated_data.get("is_active"),
        )
        SecurityValidator().validate_data(new_practice_rubric_data)
        result = model.insert_one(new_practice_rubric_data, user)
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
            lookup=["level"]
        )
        return result
