from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranWordData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    juz_id: ObjectId
    juz_seq: int
    chapter_id: ObjectId
    chapter_seq: int
    page_id: ObjectId
    page_seq: int
    line_id: ObjectId
    line_seq: int
    verse_id: ObjectId
    verse_seq: int
    sequence: int
    code: str
    chapter_name: str
    name: str
    text_madinah: str
    text_kemenag: str
    last_line: bool
    last_verse_page: bool


class QuranWordSchema(Schema):
    juz_id = ObjectIdField(required=True)
    juz_seq = ma_fields.Integer(required=True)
    chapter_id = ObjectIdField(required=True)
    chapter_seq = ma_fields.Integer(required=True)
    page_id = ObjectIdField(required=True)
    page_seq = ma_fields.Integer(required=True)
    line_id = ObjectIdField(required=True)
    line_seq = ma_fields.Integer(required=True)
    verse_id = ObjectIdField(required=True)
    verse_seq = ma_fields.Integer(required=True)
    sequence = ma_fields.Integer(required=True)
    code = ma_fields.String(required=True)
    chapter_name = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    text_madinah = ma_fields.String(required=True)
    text_kemenag = ma_fields.String(required=True)
    last_line = ma_fields.Boolean(required=True)
    last_verse_page = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranWord(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranWordData)
    collection_name = "quran_word"
    schema = QuranWordSchema
    search = ["code", "name", "chapter_name", "text_madinah", "text_kemenag"]
    object_class = QuranWordData
    foreign_key = {
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
        "line": {
            "local": "line_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_line").quran_line.QuranLine(),
        },
        "verse": {
            "local": "verse_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_verse").quran_verse.QuranVerse(),
        },
    }
