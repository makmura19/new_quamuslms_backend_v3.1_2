from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.tap_attendance_schedule import TapAttendanceSchedule, TapAttendanceScheduleData
from models.tap_attendance_group import TapAttendanceGroup
from bson import ObjectId
from datetime import datetime


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        days = set(["mon", "tue", "wed", "thu", "fri", "sat", "sun"])
        input_days = set([i.get("day") for i in value.get("schedule")])
        if days != input_days:
            raise ValidationError("Incomplete day data. Day must consist of: 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', and 'sun'")
        requered_item = ["check_in_time","check_out_time","late_after","early_leave_before"]
        for schedule in value.get("schedule"):
            for item in requered_item:
                if schedule.get("is_exists"):
                    requered_value = schedule.get(item)
                    if not requered_value:
                        raise ValidationError(f"{item} must be filled.")
                    
                    try:
                        time = datetime.strptime(requered_value, "%H:%M")
                    except ValueError:
                        raise ValidationError(f"Invalid input data ({requered_value}). Time format must be 'HH:mm'")
                    time_str = datetime.strftime(time,"%H:%M")
                    time_float = float(time_str.replace(":","."))
                    schedule.update({
                        item:time_float,
                        "is_active":True
                    })
                else:
                    schedule.update({
                        item:0,
                        "is_active":False
                    })
        
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        group_data = extra.get("tap_attendance_group")
        school_id = ObjectId(group_data.get("school_id"))
        group_id = ObjectId(validated_data.get("group_id"))
        level_id = ObjectId(validated_data.get("level_id")) if validated_data.get("level_id") else None

        old_schedule_data = model.find({"school_id": school_id,"group_id": group_id,"level_id": level_id})
        old_schedule_map = {i.get("day"): i for i in old_schedule_data}
        old_schedule_ids = [ObjectId(i.get("_id")) for i in old_schedule_data]
        if old_schedule_ids:
            model.update_many({"_id":{"$in":old_schedule_ids}},{"is_active":False})

        input_data = []
        input_ids = []
        update_data = []
        for item in validated_data.get("schedule"):
            if item.get("is_exists"):
                existing_schedule_data = old_schedule_map.get(item.get("day"))
                if not existing_schedule_data:
                    new_schedule_data = TapAttendanceScheduleData(
                        school_id=school_id,
                        group_id=group_id,
                        level_id=level_id,
                        day=item.get("day"),
                        check_in_time=item.get("check_in_time"),
                        check_out_time=item.get("check_out_time"),
                        late_after=item.get("late_after"),
                        early_leave_before=item.get("early_leave_before"),
                        for_student=group_data.get("for_student"),
                        for_teacher=group_data.get("for_teacher"),
                        is_active=True,
                    )
                    input_data.append(new_schedule_data)
                    input_ids.append(new_schedule_data._id)
                else:
                    update_data.append({
                        "_id": ObjectId(existing_schedule_data.get("_id")),
                        "set_data": {
                            "check_in_time":item.get("check_in_time"),
                            "check_out_time":item.get("check_out_time"),
                            "late_after":item.get("late_after"),
                            "early_leave_before":item.get("early_leave_before"),
                            "is_active":True
                        }
                    })
                    input_ids.append(ObjectId(existing_schedule_data.get("_id")))
                    
        if input_data:
            SecurityValidator.validate_data(input_data)
            model.insert_many(input_data)
        if update_data:
            model.update_many_different_data(update_data)
        TapAttendanceGroup().update_one(
            {"_id":group_id},
            update_data={"schedule_ids":input_ids},
            user=user
        )
        return {}
    

    @staticmethod
    def list(
        model: BaseModel, query_params, params_validation, user, headers_dict=None
    ):
        days_map = {"mon":"Senin", "tue":"Selasa", "wed":"Rabu", "thu":"Kamis", "fri":"Jum'at", "sat":"Sabtu", "sun":"Minggu"}
        time_item = ["check_in_time","check_out_time","late_after","early_leave_before"]
        
        result = model.aggregate(
            add_metadata=True,
            query_params=query_params,
            params_validation=params_validation,
            fields=query_params.get("fields"),
            exclude=query_params.get("exclude"),
        ).get("data")
        for item in result:
            for k,v in item.items():
                if k in time_item:
                    print(k,v)
                    time = str(v)
                    parts = time.split('.')
                    hour = parts[0]
                    minute = parts[1]
                    if len(minute) == 1:
                        minute += "0"
                    time = f"{hour}:{minute}"
                    try:
                        time = datetime.strptime(time, "%H:%M")
                    except ValueError:
                        raise ValidationError(f"Invalid {k} data ({v})")
                    time_str = datetime.strftime(time,"%H:%M")
                    item.update({k:time_str})
        result_map = {i.get("day"):i for i in result}
        schedule_data = []
        for day_eng, day_ind in days_map.items():
            if day_eng in result_map.keys():
                schedule_data.append({
                    "day_name":day_ind,
                    "is_exists":result_map.get(day_eng).get("is_active"),
                    **result_map.get(day_eng),
                })
            else:
                schedule_data.append({
                    "day_name":day_ind,
                    "is_exists":False,
                    "day":day_eng,
                })

        return {"data":schedule_data}