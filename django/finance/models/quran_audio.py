from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId
from marshmallow import Schema, fields as ma_fields
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class QuranAudioData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    juz_id: ObjectId
    juz_seq: int
    chapter_id: ObjectId
    chapter_seq: int
    reciter_id: ObjectId
    verse_id: ObjectId
    verse_seq: int
    url: str


class QuranAudioSchema(Schema):
    juz_id = ObjectIdField(required=True)
    juz_seq = ma_fields.Integer(required=True)
    chapter_id = ObjectIdField(required=True)
    chapter_seq = ma_fields.Integer(required=True)
    reciter_id = ObjectIdField(required=True)
    verse_id = ObjectIdField(required=True)
    verse_seq = ma_fields.Integer(required=True)
    url = ma_fields.String(required=True)
    _id = ObjectIdField(required=False, allow_none=True)


class QuranAudio(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(QuranAudioData)
    collection_name = "quran_audio"
    schema = QuranAudioSchema
    search = ["url"]
    object_class = QuranAudioData
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
        "reciter": {
            "local": "reciter_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.quran_reciter"
            ).quran_reciter.QuranReciter(),
        },
        "verse": {
            "local": "verse_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__("models.quran_verse").quran_verse.QuranVerse(),
        },
    }
