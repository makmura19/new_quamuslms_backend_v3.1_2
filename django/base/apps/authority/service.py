from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from models.res_authority import ResAuthority, ResAuthorityData
from rest_framework.exceptions import ValidationError


class MainService(BaseService):
    @staticmethod
    def create(model: ResAuthority, validated_data, extra, user, headers_dict=None):
        print(validated_data)
        new_authority_data = ResAuthorityData(
            code=validated_data.get("code"),
            name=validated_data.get("name"),
            is_school=True,
        )
        SecurityValidator.validate_data(new_authority_data)
        result = model.insert_one(new_authority_data)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }
