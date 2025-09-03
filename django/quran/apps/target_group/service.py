from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.quran_target_group import QuranTargetGroup, QuranTargetGroupData
from models.quran_target import QuranTarget
from models.quran_class import QuranClass
from bson import ObjectId
from .utils import active_academic_year

class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        
        existing_data = QuranTargetGroup().find_one({"name": value.get("name"), "program_type": value.get("program_type")})
        if existing_data:
            program = {"tahfidz": "Tahfidz", "Tahsin": "tahsin", "pra_tahsin": "Pra Tahsin"}
            raise ValidationError(f"Target Program {program.get(value.get('program_type'))} dengan nama {value.get('name')} sudah ada.")
        
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_data = QuranTargetGroupData(
            school_id=validated_data.get("school_id") if validated_data.get("school_id") else ObjectId(user.school_id),
            program_type=validated_data.get("program_type"),
            name=validated_data.get("name"),
            is_active=validated_data.get("is_active")
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
            lookup=["school","target"]
        )
        return result
    
    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        existing = QuranTargetGroup().find_one({"program_type": value.get("program_type"), "name": value.get("name")})
        if existing:
            if ObjectId(existing.get("_id")) != ObjectId(old_data.get("_id")):
                raise ValidationError(f"Target grup dengan nama {value.get('name')} sudah ada.")
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
            "message": None
        }
        
    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        from utils.id_util import IDUtil
        
        _id = IDUtil.parse(_id, model.type_id)
        if user != "quamus_superadmin":
            if ObjectId(user.school_id) != ObjectId(old_data.get("school_id")):
                raise ValidationError("Data sekolah lain tidak bisa dihapus oleh admin sekolah.")
            
        if old_data.get("target_ids"):
            MainService.validate_active_target(old_data.get("target_ids"), old_data.get("program_type"))
            
        model.soft_delete({"_id": _id}, old_data, user=user)
        
        return {}
    
    @staticmethod
    def validate_active_target(target_ids, program_type):
        targets = [ObjectId(i) for i in target_ids]
        if not targets:
            raise ValidationError("Daftar target yang akan dihapus tidak ditemukan.")
        
        target_list = QuranTarget().find({"_id": {"$in": targets}})
        
        class_ids = [ObjectId(j.get("class_id")) for j in target_list if j.get("class_id")]
        
        if class_ids:
            class_list = QuranClass().find({"_id": {"$in": class_ids}})
            if any(
                j for j in class_list
                if j.get("academic_year_id") == active_academic_year().get("_id")
            ):
                raise ValidationError(f"Data tidak dapat dihapus karena digunakan oleh kelompok {program_type} yang sedang aktif.")