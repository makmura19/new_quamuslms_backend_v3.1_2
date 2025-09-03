from dataclasses import dataclass, field
from typing import Optional
from bson import ObjectId

from marshmallow import Schema, fields as ma_fields, validate
from helpers.base_model import BaseModel
from helpers.custom_model_field import ObjectIdField
from utils.dict_util import DictUtil


@dataclass(kw_only=True)
class ConfigMutabaahData:
    _id: Optional[ObjectId] = field(default_factory=lambda: ObjectId())
    school_id: ObjectId
    use_group: bool
    use_class: bool
    score_format: str


class ConfigMutabaahSchema(Schema):
    school_id = ObjectIdField(required=True, allow_none=False)
    use_group = ma_fields.Boolean(required=True)
    use_class = ma_fields.Boolean(required=True)
    score_format = ma_fields.String(
        validate=validate.OneOf(["letter", "number"]), required=True
    )
    _id = ObjectIdField(required=False, allow_none=True)


class ConfigMutabaah(BaseModel):
    type_id = DictUtil.get_id_type_from_dataclass(ConfigMutabaahData)
    collection_name = "config_mutabaah"
    schema = ConfigMutabaahSchema
    search = ["score_format"]
    object_class = ConfigMutabaahData
    foreign_key = {
        "school": {
            "local": "school_id",
            "foreign": "_id",
            "sort": None,
            "model": lambda: __import__(
                "models.school_school"
            ).school_school.SchoolSchool(),
        }
    }
