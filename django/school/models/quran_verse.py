from dataclasses import dataclass, field
from typing import Optional, List
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranVerseData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    name: str
    sequence: int
    verse_no: int
    word_ids: Optional[List[ObjectId]] = field(default_factory=list)
    juz_id: ObjectId
    juz_seq: int
    chapter_id: ObjectId
    chapter_seq: int
    page_id: ObjectId
    page_seq: int
    arabic: str
    translation: str


class QuranVerseSchema(Schema):
    name = ma_fields.String(required=True)
    sequence = ma_fields.Integer(required=True)
    verse_no = ma_fields.Integer(required=True)
    word_ids = ma_fields.List(ObjectIdField(), required=True)
    juz_id = ObjectIdField(required=True, allow_none=False)
    juz_seq = ma_fields.Integer(required=True)
    chapter_id = ObjectIdField(required=True, allow_none=False)
    chapter_seq = ma_fields.Integer(required=True)
    page_id = ObjectIdField(required=True, allow_none=False)
    page_seq = ma_fields.Integer(required=True)
    arabic = ma_fields.String(required=True)
    translation = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranVerse(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranVerseData)
    collection_name = "quran_verse"
    schema = QuranVerseSchema
    search = ["name", "arabic", "translation"]
    object_class = QuranVerseData
    foreign_key = {
        "words": {
            "local": "word_ids",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_word").quran_word.QuranWord(),
        },
        "juz": {
            "local": "juz_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_juz").quran_juz.QuranJuz(),
        },
        "chapter": {
            "local": "chapter_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_chapter"
            ).quran_chapter.QuranChapter(),
        },
        "page": {
            "local": "page_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_page").quran_page.QuranPage(),
        },
    }
