from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.school_class import SchoolClassData
from models.edu_academic_year import EduAcademicYear
from datetime import datetime, timezone
from bson import ObjectId


class MainService(BaseService):

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        now = datetime.now(timezone.utc)
        academic_year_data = EduAcademicYear().find_one(
            {"start_date": {"$lte": now}, "end_date": {"$gte": now}}
        )
        new_class_data = SchoolClassData(
            school_id=validated_data.get("school_id"),
            academic_year_id=academic_year_data.get("_id"),
            name=validated_data.get("name"),
            homeroom_id=validated_data.get("homeroom_id"),
            level_id=validated_data.get("level_id"),
            level_sequence=extra.get("edu_stage_level").get("sequence"),
            is_active=validated_data.get("is_active"),
        )
        result = model.insert_one(new_class_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        update_class_data = {
            "name": validated_data.get("name"),
            "homeroom_id": validated_data.get("homeroom_id"),
            "level_id": validated_data.get("level_id"),
            "level_sequence": extra.get("edu_stage_level").get("sequence"),
            "is_active": validated_data.get("is_active"),
        }
        model.update_one(
            {"_id": ObjectId(_id)}, update_data=update_class_data, user=user
        )
        return {
            "data": {"id": str(_id)},
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
            lookup=["school", "academic_year", "homeroom", "level"],
        )
        return result

    @staticmethod
    def subject(
        model: BaseModel,
        _id,
        user,
        headers_dict=None,
        query_params={},
        params_validation={},
    ):
        from models.school_subject import SchoolSubject
        from models.school_class_subject import SchoolClassSubject

        class_data = model.find_one({"_id": ObjectId(_id)})
        subject_data = SchoolSubject().find(
            {
                "school_id": ObjectId(class_data.get("school_id")),
                "level_ids": ObjectId(class_data.get("level_id")),
            },
            query_params={"sort": "sequence"},
        )
        class_subject_data = SchoolClassSubject().find(
            {
                "school_id": ObjectId(class_data.get("school_id")),
                "class_id": ObjectId(_id),
                "is_active": True,
            }
        )
        class_subject_data = {
            item.get("subject_id"): item for item in class_subject_data
        }

        data = [
            {
                "_id": item.get("_id"),
                "name": item.get("name"),
                "teacher_ids": (
                    class_subject_data.get(item.get("_id")).get("teacher_ids")
                    if class_subject_data.get(item.get("_id"))
                    else []
                ),
                "is_active": (
                    True if class_subject_data.get(item.get("_id")) else False
                ),
                "threshold": (
                    class_subject_data.get(item.get("_id")).get("threshold")
                    if class_subject_data.get(item.get("_id"))
                    else 0
                ),
            }
            for item in subject_data
        ]
        return data

    @staticmethod
    def validate_update_subject(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        from models.school_subject import SchoolSubject
        from models.school_teacher import SchoolTeacher

        subject_data = SchoolSubject().find(
            {
                "school_id": ObjectId(old_data.get("school_id")),
                "level_ids": ObjectId(old_data.get("level_id")),
            }
        )
        subject_data_map = {item.get("_id"): item for item in subject_data}
        subject_data_ids = [item.get("_id") for item in subject_data]
        teacher_data = SchoolTeacher().find(
            {"school_id": ObjectId(old_data.get("school_id"))}
        )
        teacher_data = [item.get("_id") for item in teacher_data]

        for i in value.get("data", []):
            sid = i.get("_id")
            if sid not in subject_data_ids:
                raise ValueError(f"❌ Subject {sid} tidak terdaftar di sekolah ini")

            for tid in i.get("teacher_ids", []):
                if tid not in teacher_data:
                    raise ValueError(f"❌ Teacher {tid} tidak terdaftar di sekolah ini")
        extra = {"subject_data": subject_data_map}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def update_subject(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        from models.school_class_subject import (
            SchoolClassSubject,
            SchoolClassSubjectData,
        )
        from models.edu_academic_year import EduAcademicYear

        academic_year_data = EduAcademicYear().get_active()

        SchoolClassSubject().update_many(
            {
                "school_id": ObjectId(old_data.get("school_id")),
                "class_id": ObjectId(_id),
            },
            {"is_active": False},
        )
        class_subject_data = SchoolClassSubject().find(
            {
                "school_id": ObjectId(old_data.get("school_id")),
                "class_id": ObjectId(_id),
            }
        )
        class_subject_data = {
            item.get("subject_id"): item for item in class_subject_data
        }
        active_data = [
            item for item in validated_data.get("data") if item.get("is_active") == True
        ]
        input_data = []
        update_data = []
        class_subject_ids = []
        subject_ids = []
        for i in active_data:
            existing_data = class_subject_data.get(i.get("_id"))
            selected_subject = extra.get("subject_data").get(i.get("_id"))
            subject_ids.append(ObjectId(selected_subject.get("_id")))
            if existing_data:
                update_data.append(
                    {
                        "_id": existing_data.get("_id"),
                        "set_data": {
                            "is_active": True,
                            "teacher_ids": [
                                ObjectId(t) for t in i.get("teacher_ids", [])
                            ],
                            "threshold": i.get("threshold"),
                        },
                    }
                )
                class_subject_ids.append(ObjectId(existing_data.get("_id")))
            else:
                new_school_class_subject_data = SchoolClassSubjectData(
                    academic_year_id=ObjectId(academic_year_data.get("_id")),
                    school_id=ObjectId(old_data.get("school_id")),
                    class_id=ObjectId(_id),
                    teacher_ids=[ObjectId(t) for t in i.get("teacher_ids", [])],
                    subject_id=ObjectId(i.get("_id")),
                    name=selected_subject.get("name"),
                    threshold=i.get("threshold"),
                    is_sem1_submitted=False,
                    is_sem2_submitted=False,
                    is_active=True,
                )

                class_subject_ids.append(new_school_class_subject_data._id)
                input_data.append(new_school_class_subject_data)

        SecurityValidator().validate_data(input_data)

        if input_data:
            SchoolClassSubject().insert_many(input_data)
        if update_data:
            SchoolClassSubject().update_many_different_data(update_data)

        model.update_one(
            {"_id": ObjectId(_id)},
            {"class_subject_ids": class_subject_ids, "subject_ids": subject_ids},
        )

        return {
            "data": {"id": str(_id)},
            "message": None,
        }
