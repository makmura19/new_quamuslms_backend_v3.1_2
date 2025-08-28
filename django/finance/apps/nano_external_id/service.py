from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.finance_nano_external_id import FinanceNanoExternalId


class MainService(BaseService):
    pass
    # @staticmethod
    # def validate_create(value, _extra, secret, user, old_data=None):
    #     from utils.dict_util import DictUtil
    #     existing_data = FinanceNanoExternalId().find_one({"external_id":value.get("external_id")})
    #     if existing_data:
    #         raise ValidationError(f"external_id already exists.")
        
    #     extra = {}
    #     return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}
