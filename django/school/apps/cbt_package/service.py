from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.school_teacher import SchoolTeacher
from models.cbt_package import CbtPackageData
from bson import ObjectId


class MainService(BaseService):

    @staticmethod
    def validate_create_update(value, user):
        from models.edu_academic_year import EduAcademicYear
        from models.school_class_subject import SchoolClassSubject
        from models.school_class import SchoolClass

        school_id = ObjectId(user.school_id)
        teacher_data = SchoolTeacher().find_one({"login": user.username})
        teacher_id = ObjectId(teacher_data.get("_id"))
        academic_year_id = ObjectId(EduAcademicYear().get_active().get("_id"))
        class_data = SchoolClass().find(
            {
                "school_id": school_id,
                "level_id": ObjectId(value.get("level_id")),
            }
        )
        if not class_data:
            raise ValidationError(
                "Invalid level_id. Your school does not have a class for that level yet."
            )
        class_ids = [ObjectId(i.get("_id")) for i in class_data]
        class_subject_data = SchoolClassSubject().find(
            {
                "school_id": school_id,
                "academic_year_id": academic_year_id,
                "subject_id": ObjectId(value.get("subject_id")),
                "teacher_ids": teacher_id,
                "class_id": {"$in": class_ids},
            }
        )
        if not class_subject_data:
            raise ValidationError(
                "You do not have permission because you are not a teacher of the relevant subject."
            )

        return {
            "school_id": school_id,
            "teacher_id": teacher_id,
        }

    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        extra = MainService.validate_create_update(value, user)
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.edu_academic_year import EduAcademicYear
        
        academic_year_data = EduAcademicYear().get_active()
        new_package_data = CbtPackageData(
            academic_year_id=ObjectId(academic_year_data.get("_id")),
            school_id=extra.get("school_id"),
            teacher_id=extra.get("teacher_id"),
            subject_id=ObjectId(validated_data.get("subject_id")),
            edu_subject_id=ObjectId(extra.get("school_subject").get("subject_id")) if extra.get("school_subject").get("subject_id") else None,
            level_id=ObjectId(validated_data.get("level_id")),
            name=validated_data.get("name"),
            is_public=validated_data.get("is_public"),
            is_active=validated_data.get("is_active"),
        )
        SecurityValidator.validate_data(new_package_data)
        result = model.insert_one(new_package_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        extra = MainService.validate_create_update(value, user)
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

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
            lookup=["teacher", "subject", "level"],
        )
        return result
