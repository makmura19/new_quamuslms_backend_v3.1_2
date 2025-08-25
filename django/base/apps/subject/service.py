from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.edu_subject import EduSubject, EduSubjectData
from models.edu_stage_level import EduStageLevel

class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user):
        from utils.dict_util import DictUtil
        
        if EduSubject().find_one({"name": value.get("name")}):
            raise ValidationError(f"Mata pelajaran {value.get('name')} sudah dibuat.")

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        existing = model.find({})
        new_data = EduSubjectData(
            name=validated_data.get("name"),
            short_name=validated_data.get("short_name"),
            sequence=len(existing)+1,
            is_catalogue=validated_data.get("is_catalogue"),
            is_active=validated_data.get("is_active")
        )
        SecurityValidator.validate_data(new_data)
        
        result = model.insert_one(new_data, user)
        
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from utils.id_util import IDUtil

        _id = IDUtil.parse(_id, model.type_id)
        
        update_data = {
            "name": validated_data.get("name"),
            "short_name": validated_data.get("short_name"),
            "sequence": old_data.get("sequence"),
            "is_catalogue": validated_data.get("is_catalogue"),
            "is_active": validated_data.get("is_active")
        }
        
        model.update_one({"_id": _id}, update_data=update_data, user=user)
        
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
        

    @staticmethod
    def sequence(model: BaseModel, validated_data, extra, user, headers_dict=None):
        model.update_sequence(validated_data.get("_ids"))
        return {
            "message": None,
        }
        
    @staticmethod
    def validate_upload_images(value, _extra, secret, user):
        from utils.dict_util import DictUtil
        
        if not value.get("file1") and not value.get("file2"):
            raise ValidationError("Tidak ada file yang dipilih.")
        
        extra = {}
        
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}
        
    @staticmethod
    def upload_images(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from utils.id_util import IDUtil
        from utils.file_storage_util import FileStorageUtil
        
        update_data = {}
        if validated_data.get("file1"):
            if old_data.get("bar_img"):
                FileStorageUtil.delete_files(old_data.get("bar_img").split())
            bar_img_url = FileStorageUtil.upload_aws(validated_data.get("file1"),"subject_bar_img")
            if not bar_img_url:
                raise ValidationError("Upload bar image gagal.")
            update_data["bar_img"] = bar_img_url[0]
            
        if validated_data.get("file2"):
            if old_data.get("thumbnail_img"):
                FileStorageUtil.delete_files(old_data.get("thumbnail_img").split())
            thumbnail_img_url = FileStorageUtil.upload_aws(validated_data.get("file2"),"subject_thumbnail_img")
            if not thumbnail_img_url:
                raise ValidationError("Upload thumbnail image gagal.")
            update_data["thumbnail_img"] = thumbnail_img_url[0]
        
        _id = IDUtil.parse(_id, model.type_id)
        if not update_data:
            raise ValidationError("Tidak ada file yang diupload.")
        
        model.update_one({"_id": _id}, update_data=update_data, user=user)
        
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
        
    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        from utils.id_util import IDUtil

        _id = IDUtil.parse(_id, model.type_id)
        model.soft_delete({"_id": _id}, old_data, user=user)
        
        return {}