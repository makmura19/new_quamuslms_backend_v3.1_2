from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.edu_degree import EduDegreeData


class MainService(BaseService):

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        existing = model.find({})
        new_data = EduDegreeData(
            level=validated_data.get("level"),
            name=validated_data.get("name"),
            short_name=validated_data.get("short_name"),
            semester_count=validated_data.get("semester_count"),
            sequence=len(existing) + 1,
        )

        SecurityValidator.validate_data(new_data)
        result = model.insert_one(new_data, user)

        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def sequence(model: BaseModel, validated_data, extra, user, headers_dict=None):
        model.update_sequence(validated_data.get("_ids"))
        return {
            "message": None,
        }
