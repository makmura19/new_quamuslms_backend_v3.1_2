from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.quran_score_category import QuranScoreCategory, QuranScoreCategoryData
from models.quran_score_type import QuranScoreType
from bson import ObjectId


class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        existing = QuranScoreCategory().find_one({
            "school_id": ObjectId(user.school_id) if user.role == "admin" else None,
            "type_id": ObjectId(value.get("type_id")),
            "name": value.get("name")
        })
        if existing:
            raise ValidationError(f"Data kategori skor dengan nama {value.get('name')} sudah ada.")
        
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_data = QuranScoreCategoryData(
            school_id=ObjectId(user.school_id) if user.role == "admin" else None,
            type_id=ObjectId(validated_data.get("type_id")),
            name=validated_data.get("name"),
            description=validated_data.get("description"),
            penalty_point=validated_data.get("penalty_point"),
            max_score=validated_data.get("max_score"),
            min_score=validated_data.get("min_score")
        )
        SecurityValidator.validate_data(new_data)
        result = model.insert_one(new_data, user)
        QuranScoreType().update_one(
            {"_id": ObjectId(validated_data.get("type_id"))},
            add_to_set_data={"category_ids": [new_data._id]}
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
            lookup=["school","type"]
        )
        return result
    
    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        existing = QuranScoreCategory().find_one({
            "school_id": ObjectId(user.school_id) if user.role == "admin" else None,
            "type_id": ObjectId(old_data.get("type_id")),
            "name": value.get("name")
        })
        if existing:
            if ObjectId(existing.get("_id")) != ObjectId(old_data.get("_id")):
                raise ValidationError(f"Data kategori skor dengan nama {value.get('name')} sudah ada.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from utils.id_util import IDUtil

        _id = IDUtil.parse(_id, model.type_id)
        model.update_one({"_id": _id}, update_data=validated_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
        
    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        from utils.id_util import IDUtil
        
        if user.role == "superadmin" and old_data.get("school_id") is not None:
            raise ValidationError("Data milik sekolah tidak dapat dihapus oleh superadmin.")
        elif user.role != "superadmin" and old_data.get("school_id") is None:
            raise ValidationError("Data default Quamus tidak dapat dihapus.")

        _id = IDUtil.parse(_id, model.type_id)
        model.soft_delete({"_id": _id}, old_data, user=user)
        QuranScoreType().update_one(
            {"_id": ObjectId(old_data.get("type_id"))},
            pull_data={"category_ids": [ObjectId(_id)]}
        )
        
        return {}