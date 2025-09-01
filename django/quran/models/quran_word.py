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
    code: str
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
    verse_no: int
    sequence: Optional[int] = field(default=None)
    chapter_name: str
    name: str
    arabic_madinah: Optional[str] = field(default=None)
    arabic_kemenag: Optional[str] = field(default=None)
    last_line: bool
    last_verse_page: bool
    is_word: bool
    is_end: bool


class QuranWordSchema(Schema):
    code = ma_fields.String(required=True)
    juz_id = ObjectIdField(required=True, allow_none=False)
    juz_seq = ma_fields.Integer(required=True)
    chapter_id = ObjectIdField(required=True, allow_none=False)
    chapter_seq = ma_fields.Integer(required=True)
    page_id = ObjectIdField(required=True, allow_none=False)
    page_seq = ma_fields.Integer(required=True)
    line_id = ObjectIdField(required=True, allow_none=False)
    line_seq = ma_fields.Integer(required=True)
    verse_id = ObjectIdField(required=True, allow_none=False)
    verse_seq = ma_fields.Integer(required=True)
    verse_no = ma_fields.Integer(required=True)
    sequence = ma_fields.Integer(required=False, allow_none=True)
    chapter_name = ma_fields.String(required=True)
    name = ma_fields.String(required=True)
    arabic_madinah = ma_fields.String(required=False, allow_none=True)
    arabic_kemenag = ma_fields.String(required=False, allow_none=True)
    last_line = ma_fields.Boolean(required=True)
    last_verse_page = ma_fields.Boolean(required=True)
    is_word = ma_fields.Boolean(required=True)
    is_end = ma_fields.Boolean(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranWord(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranWordData)
    collection_name = "quran_word"
    schema = QuranWordSchema
    search = ["code", "name", "chapter_name", "arabic_madinah", "arabic_kemenag"]
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
