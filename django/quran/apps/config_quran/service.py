from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId
from constants.params_validation_type import ParamsValidationType


class MainService(BaseService):
    
    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        
        if _extra.get("school_teacher"):
            if str(_extra.get("school_teacher").get("school_id")) != str(old_data.get("school_id")):
                raise ValidationError(f"{_extra.get('school_teacher').get('name')} (ID {value.get('coordinator_id')}) bukan guru sekolah tersebut.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}
    

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from models.res_user import ResUser
        from models.school_teacher import SchoolTeacher
        from constants.access import Role

        old_coordinator_id = ObjectId(old_data.get("coordinator_id")) if old_data.get("coordinator_id") else None
        new_coordinator_id = ObjectId(validated_data.get("coordinator_id")) if validated_data.get("coordinator_id") else None
        update_config_quran_data = {
            "daily_assesment_rule":validated_data.get("daily_assesment_rule"),
            "exam_assesment_rule":validated_data.get("exam_assesment_rule"),
            "juziyah_assesment_rule":validated_data.get("juziyah_assesment_rule"),
            "coordinator_id":new_coordinator_id,
            "target_period":validated_data.get("target_period"),
            "exam_threshold":validated_data.get("exam_threshold"),
            "use_matrix":validated_data.get("use_matrix"),
            "multiple_class_per_student":validated_data.get("multiple_class_per_student"),
            "use_whatsapp":validated_data.get("use_whatsapp"),
            "whatsapp_no":validated_data.get("whatsapp_no"),
            "quran_type":validated_data.get("quran_type"),
        }
        role_map = {
            "tahfidz": Role.TAHFIDZ_COORDINATOR,
            "tahsin": Role.TAHSIN_COORDINATOR,
            "pra_tahsin": Role.PRA_TAHSIN_COORDINATOR
        }
        role = role_map.get(old_data.get("program_type"))
        if old_coordinator_id != new_coordinator_id:
            if old_coordinator_id:
                SchoolTeacher().pull_secondary_role(old_coordinator_id, role, user)
            if new_coordinator_id:
                user_id = extra.get("school_teacher").get("user_id")
                if user_id:
                    SchoolTeacher().add_secondary_role(new_coordinator_id, role, user)
                else:
                    SchoolTeacher().create_account(new_coordinator_id, role, user)
        model.update_one({"_id": ObjectId(_id)}, update_data=update_config_quran_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }

    @staticmethod
    def retrieve(
        model: BaseModel,
        _id,
        user,
        headers_dict=None,
        query_params={},
        params_validation={},
    ):
        result = model.aggregate(
            query_params={**query_params, "_id": ObjectId(_id)},
            params_validation={
                **params_validation,
                "_id": ParamsValidationType.OBJECT_ID,
            },
            lookup=["coordinator","teachers"]
        )
        return result[0]