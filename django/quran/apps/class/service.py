from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.quran_class import QuranClass, QuranClassData
from bson import ObjectId
from datetime import datetime, timezone
from models.edu_academic_year import EduAcademicYear
from .utils import active_academic_year


class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        
        existing = QuranClass().find_one({
            "school_id": ObjectId(value.get("school_id")),
            "academic_year_id": active_academic_year().get("_id"),
            "name": value.get("name")
        })
        if existing:
            raise ValidationError(f"Nama kelompok {value.get('name')} sudah ada.")
        
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}
    
    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        print("validate", validated_data)
        # data = model.new(**validated_data)
        # result = model.insert_one(data, user)
        return {
            # "data": {"_id": str(result.inserted_id)},
            "message": None,
        }
