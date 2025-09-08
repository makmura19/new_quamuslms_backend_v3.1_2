from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.quran_exam_content import QuranExamContent, QuranExamContentData
from models.quran_exam import QuranExam
from models.quran_juz import QuranJuz
from models.quran_chapter import QuranChapter
from models.pra_tahsin_book import PraTahsinBook
from bson import ObjectId
import json

class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        filtering = {
            "exam_id": ObjectId(value.get("exam_id")),
            "student_id": ObjectId(value.get("student_id")) if value.get("student_id") else None,
            "type": value.get("type")
        }
        if value.get("type") == "juz":
            filtering["juz_id"] = ObjectId(value.get("juz_id"))
        elif value.get("type") == "chapter":
            filtering["chapter_id"] = ObjectId(value.get("chapter_id"))
        elif value.get("type") == "book":
            filtering["book_id"] = ObjectId(value.get("book_id"))
        elif value.get("type") == "custom":
            if value.get("verse_seq_from") and value.get("verse_seq_to"):
                filtering.update({
                    "verse_seq_from": value.get("verse_seq_from"),
                    "verse_seq_to": value.get("verse_seq_to")
                })
            elif value.get("page_seq_from") and value.get("page_seq_to"):
                filtering.update({
                    "page_seq_from": value.get("page_seq_from"),
                    "page_seq_to": value.get("page_seq_to")
                })
            
        existing = QuranExamContent().find_one(filtering)
        if existing:
            raise ValidationError("Data konten ujian yang dipilih sudah ada.")
        
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}
    
    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        existing = model.find({"exam_id": ObjectId(validated_data.get("exam_id"))})
        juz_seq, chapter_seq, book_seq = MainService.create__get_sequence(
            validated_data.get("type"),
            validated_data.get(f"{validated_data.get('type')}_id")
        )
        new_data = QuranExamContentData(
            school_id=ObjectId(user.school_id) if user.role != "superadmin" else ObjectId(validated_data.get("school_id")),
            exam_id=ObjectId(validated_data.get("exam_id")),
            student_id=ObjectId(validated_data.get("student_id")) if validated_data.get("student_id") else None,
            sequence=len(existing)+1,
            type=validated_data.get("type"),
            is_student=True if validated_data.get("student_id") else False,
            juz_id=ObjectId(validated_data.get("juz_id")) if validated_data.get("juz_id") else None,
            juz_seq=juz_seq,
            chapter_id=ObjectId(validated_data.get("chapter_id")) if validated_data.get("chapter_id") else None,
            chapter_seq=chapter_seq,
            verse_seq_from=validated_data.get("verse_seq_from") if validated_data.get("verse_seq_from") else None,
            verse_seq_to=validated_data.get("verse_seq_to") if validated_data.get("verse_seq_to") else None,
            page_seq_from=validated_data.get("page_seq_from") if validated_data.get("page_seq_from") else None,
            page_seq_to=validated_data.get("page_seq_to") if validated_data.get("page_seq_to") else None,
            book_id=ObjectId(validated_data.get("book_id")) if validated_data.get("book_id") else None,
        )
        SecurityValidator.validate_data(new_data)
        result = model.insert_one(new_data, user)
        QuranExam().update_one(
            {"_id": ObjectId(validated_data.get("exam_id"))},
            add_to_set_data={"content_ids": [ObjectId(new_data._id)]}
        )
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }
        
    def create__get_sequence(type, _id):
        juz_seq = None
        chapter_seq = None
        book_seq = None
        filtering = {"_id": ObjectId(_id)}
        item = {"juz": QuranJuz, "chapter": QuranChapter, "book": PraTahsinBook}
        if type:
            data = item.get(type)().find_one(filtering)
            if data:
                sequence = data.get("sequence")
                if type == "juz":
                    juz_seq = sequence
                elif type == "chapter":
                    chapter_seq = sequence
                else:
                    book_seq = sequence
        return juz_seq, chapter_seq, book_seq
    
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
            lookup=["school","exam","juz","chapter","book"]
        )
        return result
    
    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        from utils.id_util import IDUtil

        _id = IDUtil.parse(_id, model.type_id)
        model.soft_delete({"_id": _id}, old_data, user=user)
        QuranExam().update_one(
            {"_id": ObjectId(old_data.get("exam_id"))},
            pull_data={"content_ids": [ObjectId(_id)]}
        )
        return {}
    
    @staticmethod
    def sequence(model: BaseModel, validated_data, extra, user, headers_dict=None):
        model.update_sequence(validated_data.get("_ids"))
        level_ids = [ObjectId(item) for item in validated_data.get("_ids")]
        QuranExam().update_one(
            {"_id": ObjectId(validated_data.get("exam_id"))}, {"content_ids": level_ids}
        )

        return {
            "message": None,
        }