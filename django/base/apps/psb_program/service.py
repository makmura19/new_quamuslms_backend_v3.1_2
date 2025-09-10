from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId
from models.psb_program import PsbProgram, PsbProgramData
from models.psb_psb import PsbPsb


class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        existing = PsbProgram().find_one({
            "holding_id": ObjectId(value.get("holding_id")) if value.get("holding_id") else None,
            "school_id": ObjectId(value.get("school_id")) if value.get("school_id") else None,
            "psb_id": ObjectId(value.get("psb_id")),
            "name": value.get("name"),
            "academic_year_id": ObjectId(value.get("academic_year_id"))
        })
        if existing:
            raise ValidationError("Data sudah digunakan.")
        
        if value.get("holding_id"):
            school_ids = _extra.get("school_holding",{}).get("school_ids")
            if _extra.get("psb_psb",{}).get("holding_id") != value.get("holding_id"):
                raise ValidationError("Data yayasan dan PSB tidak sesuai.")
            if _extra.get("psb_psb",{}).get("school_id") not in school_ids:
                raise ValidationError("Data sekolah dan PSB tidak sesuai.")
        elif value.get("school_id"):
            if _extra.get("psb_psb",{}).get("school_id") != value.get("school_id"):
                raise ValidationError("Data sekolah dan PSB tidak sesuai.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_program_data = PsbProgramData(
            holding_id=ObjectId(validated_data.get("holding_id")) if validated_data.get("holding_id") else None,
            school_id=ObjectId(validated_data.get("school_id")) if validated_data.get("school_id") else None,
            psb_id=ObjectId(validated_data.get("psb_id")),
            name=validated_data.get("name"),
            slug="-".join(validated_data.get("name").lower().split()),
            academic_year_id=ObjectId(validated_data.get("academic_year_id")),
            date_from=validated_data.get("date_from"),
            date_to=validated_data.get("date_to"),
            is_active=validated_data.get("is_active"),
        )
        SecurityValidator.validate_data(new_program_data)
        result = model.insert_one(new_program_data, user)
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
            lookup=["holding", "school", "psb", "academic_year"]
        )
        return result