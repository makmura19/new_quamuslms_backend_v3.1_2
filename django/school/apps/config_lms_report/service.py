from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId
from constants.params_validation_type import ParamsValidationType
from models.config_lms_report import ConfigLmsReportData


class MainService(BaseService):
    
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
            lookup=["type"]
        )
        return result[0]


    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        from utils.array_util import ArrayUtil

        if not ArrayUtil.is_unique(value.get("report_rubric"), "letter"):
            raise ValidationError("Predikat harus unik.")
        if not ArrayUtil.is_unique(value.get("report_rubric"), "name"):
            raise ValidationError("Nama harus unik.")
        sorted_rubric = sorted(value.get("report_rubric"), key=lambda x: x['lte'])
        is_correct_gap = all([(sorted_rubric[idx+1].get("gte") - i.get("lte")) == 1 for idx, i in enumerate(sorted_rubric) if idx < len(sorted_rubric)-1])
        if not is_correct_gap:
            raise ValidationError("Gap antara batas atas dan batas bawah skor harus 1.")
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def update(
        model: BaseModel, _id, old_data, validated_data, extra, user, headers_dict=None
    ):
        student_info = validated_data.get("student_info")
        header = validated_data.get("header")
        update_data = {
            "type_id":ObjectId(validated_data.get("type_id")),
            "student_info":{
                "academic_class":student_info.get("academic_class"),
                "quran_class":student_info.get("quran_class"),
                "teacher":student_info.get("teacher"),
                "semester":student_info.get("semester"),
                "academic_year":student_info.get("academic_year"),
                "nis":student_info.get("nis"),
                "nisn":student_info.get("nisn"),
                "order":[],
            },
            "header":{
                "school_logo":header.get("school_logo"),
                "quamus_logo":header.get("quamus_logo"),
                "holding_logo":header.get("holding_logo"),
                "address":header.get("address"),
                "title":header.get("title"),
                "periodic_title":header.get("periodic_title"),
                "academic_year":header.get("academic_year"),
                "order":[]
            },
            "signature":validated_data.get("signature"),
            "report_rubric":validated_data.get("report_rubric"),
        }
        model.update_one({"_id": ObjectId(_id)}, update_data=update_data, user=user)
        return {
            "data": {"id": str(_id)},
            "message": None,
        }