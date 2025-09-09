from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.mutabaah_practice_rule import MutabaahPracticeRule, MutabaahPracticeRuleData
from models.mutabaah_practice_type import MutabaahPracticeType
from models.school_class import SchoolClass
from models.edu_academic_year import EduAcademicYear
from bson import ObjectId
from utils.datetime_util import DatetimeUtil
from datetime import datetime, timezone


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        from datetime import datetime

        for item in value.get("practice"):
            practice_type_data = MutabaahPracticeType().find_one({"_id":ObjectId(item.get("type_id"))})
            if not practice_type_data:
                raise ValidationError(f"Invalid type_id {item.get('type_id')}.")
            item.update({"practice_type_data":practice_type_data})

            rule_data = MutabaahPracticeRule().find_one({
                "school_id":ObjectId(value.get("school_id")),
                "level_id":ObjectId(value.get("level_id")),
                "practice_type_id":ObjectId(item.get("type_id")),
            })
            item.update({"is_exists_before":True if rule_data else False})
            if rule_data:
                item.update({"rule_data":rule_data})

            if item.get("is_exists"):
                target_rule = practice_type_data.get("type")
                options_rule = [i.get("item") for i in practice_type_data.get("options", [])]
                target = item.get("target")
                if target_rule == "boolean" and type(target) != bool:
                    raise ValidationError(f"The target data type of {practice_type_data.get('name')} must be boolean.")
                if target_rule == "quantitative" and type(target) != int:
                    raise ValidationError(f"The target data type of {practice_type_data.get('name')} must be integer.")
                if target_rule == "options" and target not in options_rule:
                    raise ValidationError(f"The target data type of {practice_type_data.get('name')} must be: {' or '.join(options_rule)}.")
                if target_rule == "time":
                    if type(target) == str:
                        time = DatetimeUtil.from_string(target, format="%H:%M")
                        time_str = datetime.strftime(time,"%H:%M")
                        item.update({"target":time_str})
                    else:
                        raise ValidationError(f"The target data type of {practice_type_data.get('name')} must be a string with the format: hh:mm")
            
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        now = datetime.now(timezone.utc)
        academic_year_data = EduAcademicYear().find_one({
            "start_date": { "$lte": now },
            "end_date": { "$gte": now }
        })
        input_rule_data = []
        update_rule_data = []
        push_ids = []
        pull_ids = []
        for item in validated_data.get("practice"):
            if not item.get("is_exists_before") and item.get("is_exists"):
                type_data = item.get("practice_type_data")
                new_practice_rule_data = MutabaahPracticeRuleData(
                    school_id=ObjectId(validated_data.get("school_id")),
                    level_id=ObjectId(validated_data.get("level_id")),
                    practice_type_id=ObjectId(item.get("type_id")),
                    type=type_data.get("type"),
                    options=type_data.get("options"),
                    days_of_week=type_data.get("days_of_week"),
                    period=type_data.get("period"),
                    target=item.get("target"),
                    unit=type_data.get("unit"),
                    interval=type_data.get("interval"),
                    penalty_per_interval=type_data.get("penalty_per_interval"),
                    weight=item.get("weight"),
                    min_score=item.get("min_score"),
                    max_score=item.get("max_score"),
                    submitted_by=type_data.get("submitted_by"),
                    use_timeconfig=type_data.get("use_timeconfig"),
                    use_penalty=type_data.get("use_penalty"),
                    rubric_id=ObjectId(validated_data.get("rubric_id")) if validated_data.get("rubric_id") else None,
                    is_active=True
                )
                input_rule_data.append(new_practice_rule_data)
                push_ids.append(new_practice_rule_data._id)
            elif item.get("is_exists_before"):
                rule_data = item.get("rule_data")
                rule_id = ObjectId(rule_data.get("_id"))
                if not item.get("is_exists"):
                    update_rule_data.append({
                        "_id": rule_id,
                        "set_data": {
                            "is_active": False
                        },
                    })
                    pull_ids.append(rule_id)
                else:
                    update_rule_data.append({
                        "_id": rule_id,
                        "set_data": {
                            "target":item.get("target"),
                            "is_active": True
                        },
                    })
                    is_active_before = rule_data.get("is_active")
                    if not is_active_before:
                        push_ids.append(rule_id)

        if input_rule_data:
            SecurityValidator.validate_data(input_rule_data)
            model.insert_many(input_rule_data)
        if update_rule_data:
            model.update_many_different_data(update_rule_data)
        if push_ids:
            SchoolClass().update_one(
                {
                    "school_id": ObjectId(validated_data.get("school_id")),
                    "academic_year_id": ObjectId(academic_year_data.get("_id")),
                    "level_id": ObjectId(validated_data.get("level_id"))
                },
                add_to_set_data={"mutabaah_rule_ids":push_ids}
            )
        if pull_ids:
            SchoolClass().update_one(
                {
                    "school_id": ObjectId(validated_data.get("school_id")),
                    "academic_year_id": ObjectId(academic_year_data.get("_id")),
                    "level_id": ObjectId(validated_data.get("level_id"))
                },
                pull_data={"mutabaah_rule_ids":pull_ids}
            )

        return {
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
            lookup=["level","practice_type","variant","rubric"]
        )
        return result
    

    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        from utils.array_util import ArrayUtil

        if not ArrayUtil.is_unique(value.get("days_of_week")):
            raise ValidationError("Days_of_week values cannot be the same.")
        if value.get("type") == "boolean" and value.get("unit") != None and value.get("options") != []:
            raise ValidationError("For boolean type, unit and option must be empty.")
        if value.get("type") == "quantitative" and value.get("unit") == None:
            raise ValidationError("For quantitative type, unit must be filled.")
        if value.get("type") == "options" and (not value.get("options") or len(value.get("options")) == 0):
            raise ValidationError("For quantitative type, options must be filled.")
        if value.get("type") == "time" and (not value.get("interval") or not value.get("penalty_per_interval")):
            raise ValidationError(f"For time type, interval and penalty_per_interval must be filled.")

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        update_rule_data = {
            "type":validated_data.get("type"),
            "options":validated_data.get("options"),
            "days_of_week":validated_data.get("days_of_week"),
            "period":validated_data.get("period"),
            "unit":validated_data.get("unit"),
            "interval":validated_data.get("interval"),
            "penalty_per_interval":validated_data.get("penalty_per_interval"),
            "submitted_by":validated_data.get("submitted_by"),
            "use_timeconfig":True if validated_data.get("type") == "time" else False,
            "use_penalty":True if validated_data.get("type") == "time" else False,
            "rubric_id":validated_data.get("rubric_id"),
        }

        old_data = [old_data.get("type"),old_data.get("options"),old_data.get("unit")]
        new_data = [validated_data.get("type"),validated_data.get("options"),validated_data.get("unit")]
        if old_data != new_data:
            update_rule_data.update({"is_active":False})

        model.update_one({"_id": ObjectId(_id)}, update_data=update_rule_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }