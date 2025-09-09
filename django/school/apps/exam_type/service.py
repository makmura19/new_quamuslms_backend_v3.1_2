from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.lms_exam_type import LmsExamType
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        existing_data = LmsExamType().find_one({
            "school_id":ObjectId(value.get("school_id")),
            "code":value.get("code")
        })
        if existing_data:
            raise ValidationError(f"Code '{value.get('code')}' already exists.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}
