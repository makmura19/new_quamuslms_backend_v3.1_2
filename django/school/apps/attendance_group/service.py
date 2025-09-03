from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.tap_attendance_group import TapAttendanceGroup, TapAttendanceGroupData
from models.tap_attendance_schedule import TapAttendanceSchedule
from bson import ObjectId


class MainService(BaseService):

    @staticmethod
    def validate_create_update(for_student, for_teacher, value):
        if for_student == for_teacher:
            raise ValidationError("The values of 'for_student' and 'for_teacher' cannot be the same.")
        if for_teacher:
            if value.get("is_all_teacher") == None:
                raise ValidationError("is_all_teacher field must not be null.")
            if value.get("teacher_ids") == None:
                raise ValidationError("teacher_ids field must not be null.")
            if value.get("is_all_teacher") == False and not value.get("teacher_ids"):
                raise ValidationError("If is_all_teachers is false, teacher_ids must be filled in.")
            if value.get("is_all_teacher") == True and value.get("teacher_ids"):
                raise ValidationError("If is_all_teachers is true, teacher_ids must be empty.")

    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        MainService.validate_create_update(value.get("for_student"), value.get("for_teacher"), value)
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}


    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        new_attendance_group_data = TapAttendanceGroupData(
            school_id=ObjectId(validated_data.get("school_id")),
            name=validated_data.get("name"),
            for_student=True if validated_data.get("for_student") else False,
            for_teacher=True if validated_data.get("for_teacher") else False,
            teacher_ids=validated_data.get("teacher_ids") if validated_data.get("teacher_ids") else [],
            is_all_teacher=validated_data.get("is_all_teacher") if validated_data.get("is_all_teacher") else False,
            is_default=validated_data.get("is_default"),
            is_active=True if validated_data.get("for_teacher") else False,
        )
        SecurityValidator.validate_data(new_attendance_group_data)
        result = model.insert_one(new_attendance_group_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }


    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        MainService.validate_create_update(old_data.get("for_student"), old_data.get("for_teacher"), value)
        extra = {}
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
            lookup=["school","teachers","schedules"]
        )
        return result
    

    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        TapAttendanceSchedule().soft_delete_many({"_id":{"$in":old_data.get("schedule_ids")}})
        return {}


    @staticmethod
    def activate(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        if old_data.get("for_student") == False:
            raise ValidationError("This action can only be done on student type.")
        if old_data.get("is_active") == True:
            raise ValidationError("This data has been activated.")
        existing_group_data = model.find({
            "school_id":ObjectId(old_data.get("school_id")),
            "for_student":True
        })
        existing_group_ids = [ObjectId(i.get("_id")) for i in existing_group_data]

        model.update_many(
            {"_id":{"$in":existing_group_ids}},
            {"is_active":False}
        )
        model.update_one({"_id":ObjectId(_id)},{"is_active":True})
        TapAttendanceSchedule().update_many(
            {"group_id":{"$in":existing_group_ids}},
            {"is_active":False}
        )
        TapAttendanceSchedule().update_many(
            {"group_id":ObjectId(_id)},
            {"is_active":True}
        )
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
