from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.quran_class import QuranClass, QuranClassData
from bson import ObjectId
from datetime import datetime, timezone
from models.edu_academic_year import EduAcademicYear
from .utils import active_academic_year
from models.quran_target_group import QuranTargetGroup
from models.res_authority import ResAuthority
from models.res_user import ResUser
from models.school_teacher import SchoolTeacher
import json
from helpers.user_service import UserService
from models.authentication_user import AuthenticationUserData


class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        
        existing = QuranClass().find_one({
            "school_id": ObjectId(value.get("school_id")),
            "academic_year_id": ObjectId(active_academic_year().get("_id")),
            "program_type": value.get("program_type"),
            "name": value.get("name")
        })
        if existing:
            raise ValidationError(f"Nama kelompok {value.get('name')} sudah ada.")
        
        if value.get("use_template") and not value.get("target_group_id"):
            raise ValidationError(f"Template target belum dipilih.")
        
        extra = {"use_template": value.get("use_template")}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}
    
    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        target_ids = []
        if extra.get("use_template"):
            target_group = QuranTargetGroup().find_one({"_id": ObjectId(validated_data.get("target_group_id"))})
            if target_group:
                target_ids = target_group.get("target_ids")
            
        new_quran_class_data = QuranClassData(
            school_id=ObjectId(validated_data.get("school_id")),
            academic_year_id=ObjectId(active_academic_year().get("_id")),
            program_type=validated_data.get("program_type"),
            name=validated_data.get("name"),
            teacher_id=ObjectId(validated_data.get("teacher_id")),
            teacher_ids=[ObjectId(i) for i in validated_data.get("teacher_ids", [])],
            progress=0,
            student_ids=[],
            target_ids=target_ids,
            type=validated_data.get("type"),
            is_target_prerequisite=validated_data.get("is_target_prerequisite"),
            target_type=validated_data.get("target_type"),
        )
        teachers = new_quran_class_data.teacher_ids
        teachers.append(new_quran_class_data.teacher_id)
        MainService.create__add_role(teachers)
        result = model.insert_one(new_quran_class_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }
        
    @staticmethod
    def create__add_role(teachers):
        import json
        author = ResAuthority().find_one({"code":"tahfidz_teacher"})
        if not author:
            raise ValidationError("Kode authority untuk guru tahfidz tidak ditemukan.")
        
        author_id = author.get("_id")
        teacher_list = ResUser().find({"teacher_id": {"$in": teachers}})
        update_data = []
        for u in teacher_list:
            if author_id not in u.get("authority_ids"):
                update_data.append({
                    "_id": ObjectId(u.get("_id")),
                    "add_to_set_data": {
                        "authority_ids": [ObjectId(author_id)],
                        "authority_codes": ["tahfidz_teacher"]
                    }
                })
        update_user = []
        for i in teacher_list:
            authority_codes = i.get("authority_codes")
            authority_codes.append("tahfidz_teacher")
            update_user.append({
                "username": i.get("login"),
                "role": ",".join(authority_codes)
            })
        if update_data:
            ResUser().update_many_different_data(update_data)
        if update_user:
            UserService.bulk_update_users(update_user)
            
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
            lookup=["academic_year", "teacher", "teachers", "students", "targets"]
        )
        return result

