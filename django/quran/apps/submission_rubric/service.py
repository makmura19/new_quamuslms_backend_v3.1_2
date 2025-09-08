from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId
from models.quran_submission_rubric import QuranSubmissionRubric, QuranSubmissionRubricData


class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        
        if value.get("gte") >= value.get("lte") or (value.get("gte") < 0 or value.get("lte") < 0):
            raise ValidationError("Nilai tidak valid.")
        
        existing = QuranSubmissionRubric().find({
            "school_id": ObjectId(user.school_id) if user.role != "superadmin" else ObjectId(value.get("school_id")),
            "program_type": value.get("program_type")
        })
        if any(z for z in existing if z.get("name") == value.get("name")):
            raise ValidationError(f"Rubrik dengan nama {value.get('name')} sudah ada.")
        if any(
            i for i in existing
            if (i.get("gte") < value.get("gte") and value.get("gte") < i.get("lte")) or
            (i.get("gte") < value.get("lte") and value.get("lte") < i.get("lte"))
        ):
            raise ValidationError(f"Rentang nilai antara {value['gte']} - {value['lte']} beririsan dengan data rubrik lain.")

        extra = {
            "school_id": ObjectId(user.school_id) if user.role != "superadmin" else ObjectId(value.get("school_id"))
        }
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_data = QuranSubmissionRubricData(
            school_id=extra.get("school_id"),
            program_type=validated_data.get("program_type"),
            name=validated_data.get("name"),
            gte=validated_data.get("gte"),
            lte=validated_data.get("lte")
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
            lookup=["school"]
        )
        return result
    
    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        
        if value.get("gte") >= value.get("lte") or (value.get("gte") < 0 or value.get("lte") < 0):
            raise ValidationError("Nilai tidak valid.")
        
        existing = QuranSubmissionRubric().find({
            "school_id": ObjectId(user.school_id) if user.role != "superadmin" else ObjectId(value.get("school_id")),
            "program_type": old_data.get("program_type")
        })
        if next((
            _idx for _idx, i in enumerate(existing)
            if i.get("name").strip() == value.get("name").strip() and
            ObjectId(i.get("_id")) != ObjectId(old_data.get("_id"))
        ), None) is not None:
            raise ValidationError(f"Rubrik dengan nama {value.get('name')} sudah ada.")
        
        if any(
            i for i in existing
            if (i.get("gte") < value.get("gte") and value.get("gte") < i.get("lte")) or
            (i.get("gte") < value.get("lte") and value.get("lte") < i.get("lte"))
        ):
            raise ValidationError(f"Rentang nilai antara {value['gte']} - {value['lte']} beririsan dengan data rubrik lain.")
        
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
            "message": None,
        }