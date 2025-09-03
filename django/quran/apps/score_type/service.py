from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.quran_score_type import QuranScoreType, QuranScoreTypeData
from bson import ObjectId
from models.quran_score_category import QuranScoreCategory
from models.quran_score_option import QuranScoreOption


class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        
        existing = QuranScoreType().find_one({
            "school_id": ObjectId(user.school_id) if user.role != "superadmin" else (
                ObjectId(value.get("school_id")) if value.get("school_id") else None),
            "name": value.get("name"),
            "program_type": value.get("program_type")
        })
        if existing:
            raise ValidationError(f"Data tipe skor dengan nama {value.get('name')} sudah ada.")
        
        if value.get("is_fluency") is True and value.get("has_category") is True:
            raise ValidationError("Nilai kelancaran tidak disetting untuk memiliki kategori")
        
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_data = QuranScoreTypeData(
            school_id=ObjectId(user.school_id) if user.role != "superadmin" else (
                ObjectId(validated_data.get("school_id")) if validated_data.get("school_id") else None),
            name=validated_data.get("name"),
            program_type=validated_data.get("program_type"),
            type=validated_data.get("type"),
            rule=validated_data.get("rule"),
            min_score=validated_data.get("min_score"),
            max_score=validated_data.get("max_score"),
            is_daily=validated_data.get("is_daily"),
            is_exam=validated_data.get("is_exam"),
            is_juziyah=validated_data.get("is_juziyah"),
            is_fluency=validated_data.get("is_fluency"),
            is_tajweed=validated_data.get("is_tajweed"),
            is_report=validated_data.get("is_report"),
            has_category=validated_data.get("has_category"),
            total_rule=validated_data.get("total_rule"),
            penalty_point=validated_data.get("penalty_point")
        )
        SecurityValidator.validate_data(new_data)
        result = model.insert_one(new_data, user)
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
            lookup=["school", "categories", "options"]
        )
        return result

    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        existing = QuranScoreType().find_one({
            "school_id": ObjectId(old_data.get("school_id")) if old_data.get("school_id") else None,
            "name": value.get("name"),
            "program_type": old_data.get("program_type")
        })
        if existing:
            if ObjectId(existing.get("_id")) != ObjectId(old_data.get("_id")):
                raise ValidationError(f"Data tipe skor dengan nama {value.get('name')} sudah ada.")
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
        category_ids = []
        if old_data.get("category_ids"):
            category_ids = [ObjectId(i) for i in old_data.get("category_ids")]
        option_ids = []
        if old_data.get("option_ids"):
            option_ids = [ObjectId(j) for j in old_data.get("option_ids")]
            
        model.soft_delete({"_id": _id}, old_data, user=user)
        if category_ids:
            QuranScoreCategory().soft_delete_many({"_id": {"$in": category_ids}})
        if option_ids:
            QuranScoreOption().soft_delete_many({"_id": {"$in": option_ids}})
            
        return {}
