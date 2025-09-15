from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from models.quran_target import QuranTarget, QuranTargetData
from bson import ObjectId
from models.quran_juz import QuranJuz
from models.quran_chapter import QuranChapter
from models.quran_verse import QuranVerse
from models.pra_tahsin_method import PraTahsinMethod
from models.pra_tahsin_book import PraTahsinBook
from models.quran_class import QuranClass
from models.quran_target_group import QuranTargetGroup


class MainService(BaseService):
    @staticmethod
    def validate_create(value, _extra, secret, user, old_data=None):
        from utils.dict_util import DictUtil
        
        tahfidz_tahsin = ["tahfidz", "tahsin"]
        existing = {}
        filtering = {"program_type": value.get("program_type"), "tahfidz_type": value.get("tahfidz_type")}
        if value.get("program_type") in tahfidz_tahsin:
            if not value.get("tahfidz_type"):
                raise ValidationError("Tipe target dari tahfidz/tahsin belum dipilih.")
            
            if value.get("tahfidz_type") == "juz":
                if not value.get("juz_id"):
                    raise ValidationError("Juz belum dipilih.")
                filtering["juz_id"] = ObjectId(value.get("juz_id"))
            elif value.get("tahfidz_type") == "chapter":
                if not value.get("chapter_id"):
                    raise ValidationError("Surat belum dipilih.")
                filtering["chapter_id"] = value.get("chapter_id")
            elif value.get("tahfidz_type") == "verse":
                if not value.get("verse_ids"):
                    raise ValidationError("Ayat belum dipilih.")
                verses_sorted = [ObjectId(i) for i in sorted(value.get("verse_ids"))]
                filtering["verse_ids"] = verses_sorted
        else:
            if (
                not value.get("method_id") and 
                not value.get("book_id") and 
                not value.get("book_page_from") and 
                not value.get("book_page_to")
            ):
                raise ValidationError("Metode, buku dan halaman belum dipilih.")
            filtering.update({
                "method_id": value.get("method_id"),
                "book_id": value.get("book_id"),
                "book_page_from": value.get("book_page_from"),
                "book_page_to": value.get("book_page_to")
            })
            
        existing = QuranTarget().find_one(filtering)
        if existing:
            raise ValidationError("Data target sudah ada.")
            
        extra = {}
        return {"value": value, "extra": DictUtil.merge_dicts(_extra, extra)}

    @staticmethod
    def create(model: BaseModel, validated_data, extra, user, headers_dict=None):
        filter_query = {}
        if validated_data.get("group_id"):
            filter_query["group_id"] = ObjectId(validated_data.get("group_id"))
        elif validated_data.get("class_id"):
            filter_query["class_id"] = ObjectId(validated_data.get("class_id"))
        existing = QuranTarget().find(filter_query)
        
        sequence = 1
        if existing:
            sequence = len(existing)+1
            
        name, verse_count = MainService.create__generate_name(validated_data)
        new_data = QuranTargetData(
            group_id=validated_data.get("group_id") if validated_data.get("group_id") else None,
            class_id=validated_data.get("class_id") if validated_data.get("class_id") else None,
            school_id=ObjectId(validated_data.get("school_id")) if validated_data.get("school_id") else ObjectId(user.school_id),
            name=name,
            short_name=name,
            program_type=validated_data.get("program_type"),
            tahfidz_type=validated_data.get("tahfidz_type"),
            juz_id=validated_data.get("juz_id",None),
            chapter_id=validated_data.get("chapter_id",None),
            verse_ids=validated_data.get("verse_ids",[]),
            verse_count =verse_count,
            method_id=validated_data.get("method_id",None),
            book_id=validated_data.get("book_id",None),
            book_page_from=validated_data.get("book_page_from",0),
            book_page_to=validated_data.get("book_page_to",0),
            sequence=sequence,
            is_group=True if validated_data.get("group_id") else False,
            is_class=True if validated_data.get("class_id") else False,
            is_active=validated_data.get("is_active",False)
        )
        SecurityValidator.validate_data(new_data)
        result = model.insert_one(new_data, user)
        if validated_data.get("class_id"):
            push_data = {}
            if validated_data.get("program_type") == "tahfidz":
                push_data = {"tahfidz_target_ids": [new_data._id]}
            elif validated_data.get("program_type") == "tahsin":
                push_data = {"tahsin_target_ids": [new_data._id]}
            else:
                push_data = {"pra_tahsin_target_ids": [new_data._id]}
            QuranClass().update_one(
                {"_id": ObjectId(validated_data.get("class_id"))},
                add_to_set_data=push_data
            )
        elif validated_data.get("group_id"):
            QuranTargetGroup().update_one(
                {"_id": ObjectId(validated_data.get("group_id"))},
                add_to_set_data={"target_ids": [new_data._id]}
            )
            
        return {
            "data": {"_id": str(result.inserted_id)},
            "message": None,
        }
        
    def create__generate_name(validated_data):
        item_dict = {
            "_id":i for i, j in validated_data.items()
            if i.split("_")[0] == validated_data.get("tahfidz_type") and
            validated_data.get("program_type") in ["tahfidz", "tahsin"]
        }
        if not item_dict:
            item_dict = {"_id": "book_id"}
        value = validated_data.get(item_dict.get("_id"))
        item_dict.update({
            "value": ObjectId(value) if not isinstance(value, list) else [ObjectId(v) for v in value]
        })
        items = {
            "juz_id": QuranJuz,
            "chapter_id": QuranChapter,
            "verse_ids": QuranVerse,
            "book_id": PraTahsinBook
        }
        name = "-"
        verse_count = 0
        for k, v in items.items():
            if k == item_dict.get("_id"):
                if k != "verse_ids":
                    data = v().find_one({"_id": item_dict.get("value")})
                    name = data.get("name","-")
                    if k == "chapter_id":
                        name = f"Surat {data.get('name',{}).get('latin')}"
                        
                    if k == "book_id":
                        verse_count = (validated_data.get("book_page_to") - validated_data.get("book_page_from")) + 1
                    else:
                        verse_count = data.get("verse_count",0)
                else:
                    data = v().find({"_id": {"$in": item_dict.get("value")}})
                    verses = sorted(data, key=lambda z:z.get("verse_no"))
                    if len(verses)>1:
                        name = f"{verses[0].get('name')} - {verses[-1].get('verse_no')}"
                        verse_count = len(verses)
                    else:
                        name = verses[0].get('name')
                        verse_count = 1
        return name, verse_count
    
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
            lookup=["group", "class", "school", "juz", "chapter", "verses"]
        )
        return result
    
    @staticmethod
    def destroy(model: BaseModel, _id, old_data, user, headers_dict=None):
        from utils.id_util import IDUtil
        _id = IDUtil.parse(_id, model.type_id)
        if old_data.get("group_id"):
            QuranTargetGroup().update_one(
                {"_id": ObjectId(old_data.get("group_id"))},
                pull_data={"target_ids": [ObjectId(_id)]}
            )
        model.soft_delete({"_id": _id}, old_data, user=user)
        return {}
    
    @staticmethod
    def sequence(model: BaseModel, validated_data, extra, user, headers_dict=None):
        model.update_sequence(validated_data.get("_ids"))
        return {
            "message": None,
        }