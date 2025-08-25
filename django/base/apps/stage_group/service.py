from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from models.edu_stage_group import EduStageGroupData
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError


class MainService(BaseService):
    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        print(validated_data)
        seq = model.count_data() + 1
        new_edu_stage_data = EduStageGroupData(
            name=validated_data.get("name"),
            description=validated_data.get("description"),
            sequence=seq,
            has_degree=validated_data.get("has_degree"),
            has_faculty=validated_data.get("has_faculty"),
            has_subject_mapping=validated_data.get("has_subject_mapping"),
            has_major=validated_data.get("has_major"),
            has_program_type=validated_data.get("has_program_type"),
            duration_years=validated_data.get("duration_years"),
            student_label=validated_data.get("student_label"),
        )
        SecurityValidator.validate_data(new_edu_stage_data)
        result = model.insert_one(new_edu_stage_data)
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
            lookup=["stage", "level"],
        )
        return result

    @staticmethod
    def sequence(model: BaseModel, validated_data, extra, user, headers_dict=None):
        model.update_sequence(validated_data.get("_ids"))
        return {
            "message": None,
        }
