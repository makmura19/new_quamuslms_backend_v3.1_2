from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.quran_exam import QuranExam, QuranExamData
from models.quran_exam_content import QuranExamContent
from models.quran_submission import QuranSubmission
from bson import ObjectId
from .utils import Utils
utility = Utils() 

class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        
        existing = QuranExam().find_one({
            "school_id": ObjectId(user.school_id),
            "name": value.get("name"),
            "program_type": value.get("program_type"),
            "academic_year_id": ObjectId(utility.active_academic_year().get("_id")),
            "semester_id": ObjectId(utility.active_semester().get("_id"))
        })
        if existing:
            raise ValidationError(f"Data ujian dengan nama {value.get('name')} di program {value.get('program_type')} sudah ada.")
        
        extra = {
            "academic_year_id": ObjectId(utility.active_academic_year().get("_id")),
            "semester_id": ObjectId(utility.active_semester().get("_id"))
        }
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        
        new_quran_exam_data = QuranExamData(
            school_id=ObjectId(user.school_id),
            academic_year_id=extra.get("academic_year_id"),
            semester_id=extra.get("semester_id"),
            examiner_ids=[ObjectId(eid) for eid in validated_data.get("examiner_ids", [])],
            class_ids=[ObjectId(cid) for cid in validated_data.get("class_ids", [])],
            date_from=validated_data.get("date_from"),
            date_to=validated_data.get("date_to"),
            is_open=validated_data.get("is_open"),
            code=MainService.create__generate_code(
                user.school_id if user.role != "superadmin" else validated_data.get("school_id"),
                validated_data.get("program_type")
            ),
            name=validated_data.get("name"),
            verse_count=0,
            is_score_recap=validated_data.get("is_score_recap"),
            is_multiple_submission=validated_data.get("is_multiple_submission"),
            is_entire_verses=validated_data.get("is_entire_verses"),
            is_shuffle=validated_data.get("is_shuffle"),
            content_ids=[ObjectId(cid) for cid in validated_data.get("content_ids", [])],
            program_type=validated_data.get("program_type"),
        )

        SecurityValidator.validate_data(new_quran_exam_data)
        result = model.insert_one(new_quran_exam_data, user)
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }
        
    def create__generate_code(school_id, program_type):
        prefix = {"tahfidz": "TF", "tahsin": "TH", "pra_tahsin": "PT"}
        active_exam = QuranExam().find({
            "school_id": ObjectId(school_id),
            "program_type": program_type,
            "academic_year_id": ObjectId(utility.active_academic_year().get("_id")),
            "semester_id": ObjectId(utility.active_semester().get("_id"))
        })
        
        return f"{prefix[program_type]}-{str(len(active_exam)+1).zfill(3)}"
    
    def create__update_role(teacher_ids):
        pass
    
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
            lookup=["academic_year","semester", "examiners", "classes", "contents"]
        )
        return result
    
    @staticmethod
    def validate_update(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil

        existing = QuranExam().find_one({
            "school_id": ObjectId(user.school_id),
            "name": value.get("name"),
            "program_type": old_data.get("program_type"),
            "academic_year_id": ObjectId(utility.active_academic_year().get("_id")),
            "semester_id": ObjectId(utility.active_semester().get("_id"))
        })
        if existing:
            if ObjectId(existing.get("_id")) != ObjectId(old_data.get("_id")):
                raise ValidationError(f"Paket ujian dengan nama {value.get('name')} di program {old_data.get('program_type')} sudah ada.")
        
        extra = {
            "academic_year_id": ObjectId(utility.active_academic_year().get("_id")),
            "semester_id": ObjectId(utility.active_semester().get("_id"))
        }
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
        
    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        
        from utils.id_util import IDUtil
        
        exam_content = QuranExamContent().find_one({"exam_id": ObjectId(_id)})
        exam_submission = QuranSubmission().find_one({"exam_id": ObjectId(_id)})
        if exam_content or exam_submission:
            raise ValidationError("Paket ujian tidak dapat dihapus karena sudah digunakan dalam materi ujian.")

        _id = IDUtil.parse(_id, model.type_id)
        model.soft_delete({"_id": _id}, old_data, user=user)
        return {}
