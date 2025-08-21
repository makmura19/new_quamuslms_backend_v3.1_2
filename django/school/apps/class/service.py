from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.school_class import SchoolClassData
from models.edu_academic_year import EduAcademicYear
from datetime import datetime, timezone
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        now = datetime.now(timezone.utc)
        academic_year_data = EduAcademicYear().find_one({
            "start_date": { "$lte": now },
            "end_date": { "$gte": now }
        })
        new_class_data = SchoolClassData(
            school_id=validated_data.get("school_id"),
            academic_year_id=academic_year_data.get("_id"),
            name=validated_data.get("name"),
            homeroom_id=validated_data.get("homeroom_id"),
            level_id=validated_data.get("level_id"),
            level_sequence=extra.get("edu_stage_level").get("sequence"),
        )
        result = model.insert_one(new_class_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }


    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        update_class_data = {
            "name":validated_data.get("name"),
            "homeroom_id":validated_data.get("homeroom_id"),
            "level_id":validated_data.get("level_id"),
            "level_sequence":extra.get("edu_stage_level").get("sequence"),
        }
        model.update_one({"_id": ObjectId(_id)}, update_data=update_class_data, user=user)
        return {
            "data": {"id": str(_id)},
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
            lookup=["school","academic_year","homeroom","level"]
        )
        return result
