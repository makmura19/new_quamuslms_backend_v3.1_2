from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.tap_attendance_schedule import TapAttendanceSchedule, TapAttendanceScheduleData
from models.tap_attendance_group import TapAttendanceGroup
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        existing_data = TapAttendanceSchedule().find_one({
            "school_id":ObjectId(_extra.get("tap_attendance_group").get("school_id")),
            "group_id":ObjectId(value.get("group_id")),
            "level_id":ObjectId(value.get("level_id")) if value.get("level_id") else None,
            "day":value.get("day"),
        })
        if existing_data:
            raise ValidationError(f"Data for this combination already exists.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        group_data = extra.get("tap_attendance_group")
        new_schedule_data = TapAttendanceScheduleData(
            school_id=ObjectId(group_data.get("school_id")),
            group_id=ObjectId(validated_data.get("group_id")),
            level_id=ObjectId(validated_data.get("level_id")) if validated_data.get("level_id") else None,
            day=validated_data.get("day"),
            check_in_time=validated_data.get("check_in_time"),
            check_out_time=validated_data.get("check_out_time"),
            late_after=validated_data.get("late_after"),
            early_leave_before=validated_data.get("early_leave_before"),
            for_student=group_data.get("for_student"),
            for_teacher=group_data.get("for_teacher"),
            is_active=group_data.get("is_active"),
        )
        SecurityValidator.validate_data(new_schedule_data)
        
        result = model.insert_one(new_schedule_data, user)
        TapAttendanceGroup().update_one(
            {"_id":ObjectId(validated_data.get("group_id"))},
            add_to_set_data={"schedule_ids":[new_schedule_data._id]},
            user=user
        )
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }


    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        existing_data = TapAttendanceSchedule().find_one({
            "_id":{"$ne":ObjectId(old_data.get("_id"))},
            "school_id":ObjectId(old_data.get("school_id")),
            "group_id":ObjectId(old_data.get("group_id")),
            "level_id":ObjectId(value.get("level_id")) if value.get("level_id") else None,
            "day":value.get("day"),
        })
        if existing_data:
            raise ValidationError(f"Data for this combination already exists.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}


    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        TapAttendanceGroup().update_one(
            {"_id":ObjectId(old_data.get("group_id"))},
            pull_data={"schedule_ids":[ObjectId(_id)]},
            user=user
        )
        return {}
    

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
            lookup=["school","group","level"]
        )
        return result