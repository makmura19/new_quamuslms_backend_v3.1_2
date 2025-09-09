from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.cbt_question import CbtQuestionData
from models.cbt_question_option import CbtQuestionOption, CbtQuestionOptionData
from models.school_teacher import SchoolTeacher
from utils.array_util import ArrayUtil
from bson import ObjectId

class MainService(BaseService):
    
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        if not ArrayUtil.is_unique(value.get("option_list"), "option"):
            raise ValidationError("Questions may not be duplicated.")
        is_true_list = [i.get("is_true") for i in value.get("option_list")]
        if is_true_list.count(True) != 1:
            raise ValidationError("The number of correct answers must be one.")
        if value.get("level_id") not in _extra.get("school_subject").get("level_ids"):
            raise ValidationError("Invalid level_id. The selected subject is not available for that level.")
        if _extra.get("edu_chapter"):
            if _extra.get("edu_chapter").get("level_id") != value.get("level_id"):
                raise ValidationError("Invalid chapter_id. Chapter not for that level.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        school_id = ObjectId(user.school_id)
        teacher_data = SchoolTeacher().find_one({"login":user.username})
        teacher_id = ObjectId(teacher_data.get("_id"))
        edu_subject_id = None
        if extra.get("school_subject"):
            edu_subject_id = ObjectId(extra.get("school_subject").get("subject_id")) if extra.get("school_subject").get("subject_id") else None
        question_id = ObjectId()

        new_option_data_list = []
        option_ids = []
        answer_id = None
        for item in validated_data.get("option_list"):
            new_option_data = CbtQuestionOptionData(
                school_id=school_id,
                question_id=question_id,
                text=item.get("option"),
                is_correct=item.get("is_true"),
            )
            new_option_data_list.append(new_option_data)
            option_ids.append(new_option_data._id)
            if item.get("is_true"):
                answer_id = new_option_data._id

        new_question_data = CbtQuestionData(
            _id=question_id,
            school_id=school_id,
            teacher_id=teacher_id,
            type_id=ObjectId("68b8d15e35bbaf099ee8aa80"), # Multiple Choice Single Answer
            school_subject_id=ObjectId(validated_data.get("school_subject_id")),
            edu_subject_id=edu_subject_id,
            level_id=ObjectId(validated_data.get("level_id")) if validated_data.get("level_id") else None,
            chapter_id=ObjectId(validated_data.get("chapter_id")) if validated_data.get("chapter_id") else None,
            difficulty=validated_data.get("difficulty"),
            text=validated_data.get("text"),
            option_ids=option_ids,
            answer_id=answer_id,
            answer_ids=[],
            score=validated_data.get("score"),
            is_public=validated_data.get("is_public"),
            is_active=validated_data.get("is_active"),
        )
        SecurityValidator.validate_data(new_question_data, new_option_data_list)
        result = model.insert_one(new_question_data, user)
        CbtQuestionOption().insert_many(new_option_data_list)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        from models.school_subject import SchoolSubject
        from models.edu_chapter import EduChapter

        existing_option_data = CbtQuestionOption().find({"question_id":ObjectId(old_data.get("_id"))}) 
        existing_option_ids = [i.get("_id") for i in existing_option_data]
        for item in value.get("option_list"):
            input_option_id = item.get("_id")
            if input_option_id == None:
                item.update({"status": "create"})
            elif input_option_id in existing_option_ids:
                item.update({"status": "update"})
                existing_option_ids.remove(input_option_id)
            elif input_option_id not in existing_option_ids:
                raise ValidationError(f"Invalid option_id ({input_option_id}).")
        for id in existing_option_ids:
            value["option_list"].append({
                "_id":id,
                "status": "delete"
            })
        if not ArrayUtil.is_unique(value.get("option_list"), "option"):
            raise ValidationError("Questions may not be duplicated.")
        is_true_list = [i.get("is_true") for i in value.get("option_list")]
        if is_true_list.count(True) != 1:
            raise ValidationError("The number of correct answers must be one.")
        subject_data = SchoolSubject().find_one({"_id": ObjectId(old_data.get("school_subject_id"))})
        if value.get("level_id") not in subject_data.get("level_ids"):
            raise ValidationError("Invalid level_id. The selected subject is not available for that level.")
        if value.get("chapter_id"):
            chapter_data = EduChapter().find_one({"_id": ObjectId(value.get("chapter_id"))})
            if not chapter_data:
                raise ValidationError("Invalid chapter_id.")
            if chapter_data.get("level_id") != value.get("level_id"):
                raise ValidationError("Invalid chapter_id. Chapter not for that level.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        school_id = ObjectId(user.school_id)
        new_option_data_list = []
        update_option_data_list = []
        option_ids = []
        delete_option_ids = []
        answer_id = None
        for item in validated_data.get("option_list"):
            if item.get("status") == "delete":
                delete_option_ids.append(ObjectId(item.get("_id")))
            else:
                option_id = None
                if item.get("status") == "create":
                    new_option_data = CbtQuestionOptionData(
                        school_id=school_id,
                        question_id=ObjectId(_id),
                        text=item.get("option"),
                        is_correct=item.get("is_true"),
                    )
                    new_option_data_list.append(new_option_data)
                    option_id = new_option_data._id
                elif item.get("status") == "update":
                    option_id = ObjectId(item.get("_id"))
                    update_option_data_list.append({
                        "_id": option_id,
                        "set_data": {
                            "text":item.get("option"),
                            "is_correct":item.get("is_true")
                        }
                    })
                option_ids.append(option_id)
                if item.get("is_true"):
                    answer_id = option_id
        update_question_data = {
            "level_id":ObjectId(validated_data.get("level_id")) if validated_data.get("level_id") else None,
            "chapter_id":ObjectId(validated_data.get("chapter_id")) if validated_data.get("chapter_id") else None,
            "difficulty":validated_data.get("difficulty"),
            "text":validated_data.get("text"),
            "option_ids":option_ids,
            "answer_id":answer_id,
            "score":validated_data.get("score"),
            "is_public":validated_data.get("is_public"),
            "is_active":validated_data.get("is_active"),
        }

        model.update_one({"_id": ObjectId(_id)}, update_data=update_question_data, user=user)
        if new_option_data_list:
            SecurityValidator.validate_data(new_option_data_list)
            CbtQuestionOption().insert_many(new_option_data_list)
        if update_option_data_list:
            CbtQuestionOption().update_many_different_data(update_option_data_list)
        if delete_option_ids:
            CbtQuestionOption().soft_delete_many({"_id":{"$in":delete_option_ids}})        
        return {
            "data": {"id": str(_id)},
            "message": None,
        }
    

    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        model.soft_delete({"_id": ObjectId(_id)}, old_data, user=user)
        option_ids = [ObjectId(i) for i in old_data.get("option_ids")]
        CbtQuestionOption().soft_delete_many({"_id":{"$in":option_ids}})        
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
            lookup=["options","answer","answers"]
        )
        return result