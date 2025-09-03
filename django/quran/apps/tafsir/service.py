from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.quran_tafsir import QuranTafsir


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        existing_code = QuranTafsir().find_one({"code":value.get("code")})
        if existing_code:
            raise ValidationError(f"Code '{value.get('code')}' already exists.")

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

