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
                target_ids = [ObjectId(i) for i in target_group.get("target_ids")]
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
        teachers = [ObjectId(validated_data.get("teacher_id"))]+[ObjectId(i) for i in validated_data.get("teacher_ids", [])]
        update_res_user, update_psql_user = MainService.create__add_role(teachers)
        result = model.insert_one(new_quran_class_data, user)
        if update_res_user:
            ResUser().update_many_different_data(update_res_user)
        if update_psql_user:
            UserService.bulk_update_users(update_psql_user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None
        }
        
    @staticmethod
    def create__add_role(teachers):
        author = ResAuthority().find_one({"code":"tahfidz_teacher"})
        if not author:
            raise ValidationError("Kode authority untuk guru tahfidz tidak ditemukan.")
        
        author_id = author.get("_id")
        teacher_list = ResUser().find({"teacher_id": {"$in": teachers}})
        update_res_user = []
        update_psql_user = []
        for u in teacher_list:
            if author_id not in u.get("authority_ids"):
                update_res_user.append({
                    "_id": ObjectId(u.get("_id")),
                    "add_to_set_data": {
                        "authority_ids": [ObjectId(author_id)],
                        "authority_codes": ["tahfidz_teacher"]
                    }
                })
                authority_codes = u.get("authority_codes")
                authority_codes.append("tahfidz_teacher")
                update_psql_user.append({
                    "username": u.get("login"),
                    "role": ",".join(authority_codes)
                })
        return update_res_user, update_psql_user
            
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
    
    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        existing = QuranClass().find_one({
            "school_id": ObjectId(value.get("school_id")),
            "academic_year_id": ObjectId(active_academic_year().get("_id")),
            "program_type": value.get("program_type"),
            "name": value.get("name")
        })
        if existing:
            if ObjectId(existing.get("_id")) != ObjectId(old_data.get("_id")):
                raise ValidationError(f"Nama kelompok {value.get('name')} sudah ada.")
        
        if value.get("use_template") and not value.get("target_group_id"):
            raise ValidationError(f"Template target belum dipilih.")
        
        extra = {"use_template": value.get("use_template")}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from utils.id_util import IDUtil
        
        if extra.get("use_template"):
            target_group = QuranTargetGroup().find_one({"_id": ObjectId(validated_data.get("target_group_id"))})
            if target_group:
                target_ids = [ObjectId(i) for i in target_group.get("target_ids")]
        else:
            if old_data.get("target_ids"):
                target_ids = []
                
        validated_data.update({"target_ids": [ObjectId(i) for i in target_ids]})
        
        old_tahfidz_teacher = [str(old_data.get("teacher_id"))] + [str(i) for i in old_data.get("teacher_ids")]
        new_tahfidz_teacher = [str(validated_data.get("teacher_id"))] + [str(i) for i in validated_data.get("teacher_ids")]
        add_role_data, add_role_user, rmv_role_data, rmv_role_user = MainService.update__teacher_role(
            _id,
            extra.get("school_school",{}).get("_id"),
            old_tahfidz_teacher, 
            new_tahfidz_teacher,
            "tahfidz_teacher"
        )
        _id = IDUtil.parse(_id, model.type_id)
        model.update_one({"_id": _id}, update_data=validated_data, user=user)
        
        if add_role_data:
            ResUser().update_many_different_data(add_role_data)
        if add_role_user:
            UserService.bulk_update_users(add_role_user)
            
        if rmv_role_data:
            ResUser().update_many_different_data(rmv_role_data)
        if rmv_role_user:
            UserService.bulk_update_users(rmv_role_user)
            
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
        
    def update__teacher_role(_id, school_id, old_teacher, new_teacher, code):
        author = ResAuthority().find_one({"code": code})
        if not author:
            raise ValidationError("Kode authority untuk guru tahfidz tidak ditemukan.")
        
        new_teacher_role = ResUser().find({"teacher_id": {"$in": [ObjectId(i) for i in new_teacher]}})
        teacher_add_role = [
            i for i in new_teacher_role if "tahfidz_teacher" not in i.get("authority_codes")
        ]
        add_role_data, add_role_user = MainService.update__add_role(teacher_add_role, author)
        
        candidate_rmv = [t for t in old_teacher if t not in new_teacher]
        rmv_role_data, rmv_role_user = MainService.update__remove_role(
            _id,
            school_id,
            active_academic_year().get("_id"),
            candidate_rmv,
            author
        )
            
        return add_role_data, add_role_user, rmv_role_data, rmv_role_user
    
    def update__add_role(add_list, author):
        add_role_data = []
        add_role_user = []
        for i in add_list:
            add_role_data.append({
                "_id": ObjectId(i.get("_id")),
                "add_to_set_data": {
                    "authority_ids": [ObjectId(author.get("_id"))],
                    "authority_codes": ["tahfidz_teacher"]
                }
            })
            authority_codes = i.get("authority_codes")
            authority_codes.append("tahfidz_teacher")
            add_role_user.append({
                "username": i.get("login"),
                "role": ",".join(authority_codes)
            })
            
        return add_role_data, add_role_user
    
    def update__remove_role(class_id, school_id, academic_year_id, rmv_list, author):
        other_classes = QuranClass().find({
            "_id": {"$ne": ObjectId(class_id)},
            "school_id": ObjectId(school_id),
            "academic_year_id": ObjectId(academic_year_id)
        })
        rmv_teacher = []
        for j in rmv_list:
            if not any(
                k for k in other_classes
                if k.get("teacher_id") == j or
                j in k.get("teacher_ids")
            ):
                rmv_teacher.append(j)
                
        rmv_teacher_role = []
        if rmv_teacher:
            rmv_teacher_role = ResUser().find({"teacher_id": {"$in": [ObjectId(i) for i in rmv_teacher]}})
        
        rmv_role_data = []
        rmv_role_user = []
        for k in rmv_teacher_role:
            rmv_role_data.append({
                "_id": ObjectId(k.get("_id")),
                "pull_data": {
                    "authority_ids": [ObjectId(author.get("_id"))],
                    "authority_codes": ["tahfidz_teacher"]
                }
            })
            authority_codes = k.get("authority_codes",[])
            idx = authority_codes.index("tahfidz_teacher")
            authority_codes.pop(idx)
            rmv_role_user.append({
                "username": k.get("login"),
                "role": ",".join(authority_codes)
            })
        return rmv_role_data, rmv_role_user
    
    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        from utils.id_util import IDUtil

        author = ResAuthority().find_one({"code": "tahfidz_teacher"})
        if not author:
            raise ValidationError("Kode authority untuk guru tahfidz tidak ditemukan.")
        
        _id = IDUtil.parse(_id, model.type_id)
        teacher_list = [str(old_data.get("teacher_id"))]+[str(i) for i in old_data.get("teacher_ids")]
        rmv_role_data, rmv_role_user = MainService.update__remove_role(
            _id, 
            old_data.get("school_id"),
            old_data.get("academic_year_id"),
            teacher_list,
            author
        )
        model.soft_delete({"_id": _id}, old_data, user=user)
        if rmv_role_data:
            ResUser().update_many_different_data(rmv_role_data)
        if rmv_role_user:
            UserService.bulk_update_users(rmv_role_user)
        
        return {}

