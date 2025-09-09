from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.mutabaah_practice_variant import MutabaahPracticeVariant, MutabaahPracticeVariantData
from models.mutabaah_practice_rule import MutabaahPracticeRule
from bson import ObjectId


class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        list_of_variant = [
            [str(i.get("gender")), str(i.get("is_boarding"))]
            for i in value.get("variant")
        ]
        unique_tuples = set(tuple(sorted(i)) for i in list_of_variant)
        are_lists_unique = len(unique_tuples) == len(list_of_variant)
        if not are_lists_unique:
            raise ValidationError("Variations must be unique.")
        
        existing_data = MutabaahPracticeVariant().find({
            "school_id":ObjectId(value.get("school_id")),
            "rule_id":ObjectId(value.get("rule_id")),
        })
        existing_variants = [
            {
                "gender":i.get("gender"),
                "is_boarding":i.get("is_boarding"),
            }
            for i in existing_data
        ]
        input_variants = [
            {
                "gender":i.get("gender"),
                "is_boarding":i.get("is_boarding"),
            }
            for i in value.get("variant")
        ]
        new_variant = [i for i in input_variants if i not in existing_variants]
        delete_variant_ids = [
            ObjectId(existing_data[idx].get("_id"))
            for idx, i in enumerate(existing_variants) 
            if i not in input_variants
        ]
        value.update({"new_variant":new_variant,"delete_variant_ids":delete_variant_ids})
        value.pop("variant")

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        rule_data = extra.get("mutabaah_practice_rule")
        input_data = []
        if validated_data.get("new_variant"):
            for item in validated_data.get("new_variant"):
                new_variant_data = MutabaahPracticeVariantData(
                    school_id=ObjectId(validated_data.get("school_id")),
                    practice_id=ObjectId(rule_data.get("practice_type_id")),
                    rule_id=ObjectId(validated_data.get("rule_id")),
                    level_id=ObjectId(rule_data.get("level_id")),
                    gender=item.get("gender"),
                    is_boarding=item.get("is_boarding"),
                    type=rule_data.get("type"),
                    unit=rule_data.get("unit"),
                    target=rule_data.get("target"),
                    options=rule_data.get("options"),
                    days_of_week=rule_data.get("days_of_week"),
                    period=rule_data.get("period"),
                    interval=rule_data.get("interval"),
                    penalty_per_interval=rule_data.get("penalty_per_interval"),
                    weight=rule_data.get("weight"),
                    min_score=rule_data.get("min_score"),
                    max_score=rule_data.get("max_score"),
                    submitted_by=rule_data.get("submitted_by"),
                    rubric_id=ObjectId(validated_data.get("rubric_id")) if validated_data.get("rubric_id") else None,
                    use_timeconfig=rule_data.get("use_timeconfig"),
                    use_penalty=rule_data.get("use_penalty"),
                )
                input_data.append(new_variant_data)

        variant_ids = [i._id for i in input_data]
        SecurityValidator.validate_data(input_data)
        delete_ids = validated_data.get("delete_variant_ids")
        
        if input_data:
            model.insert_many(input_data)
            MutabaahPracticeRule().update_one(
                {"_id":ObjectId(validated_data.get("rule_id"))},
                add_to_set_data={"variant_ids":variant_ids}
            )
        if delete_ids:
            model.soft_delete_many({"_id":{"$in":delete_ids}})
            MutabaahPracticeRule().update_one(
                {"_id":ObjectId(validated_data.get("rule_id"))},
                pull_data={"variant_ids":delete_ids}
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
            lookup=["rule","level","rubric"]
        )
        return result
    

    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        from utils.array_util import ArrayUtil
        from datetime import datetime
        from utils.datetime_util import DatetimeUtil

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

        target_rule = value.get("type")
        options_rule = [i.get("item") for i in value.get("options", [])]
        target = value.get("target")
        if target_rule == "boolean" and type(target) != bool:
            raise ValidationError(f"The target data type must be boolean.")
        if target_rule == "quantitative" and type(target) != int:
            raise ValidationError(f"The target data type must be integer.")
        if target_rule == "options" and target not in options_rule:
            raise ValidationError(f"The target data type must be: {' or '.join(options_rule)}.")
        if target_rule == "time":
            if type(target) == str:
                time = DatetimeUtil.from_string(target, format="%H:%M")
                time_str = datetime.strftime(time,"%H:%M")
                value.update({"target":time_str})
            else:
                raise ValidationError(f"The target data type must be a string with the format: hh:mm")
            

        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        update_variant_data = {
            "type":validated_data.get("type"),
            "target":validated_data.get("target"),
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
        model.update_one({"_id": ObjectId(_id)}, update_data=update_variant_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
    
