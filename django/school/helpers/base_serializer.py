from rest_framework import serializers
from helpers.custom_model_field import ObjectIdField, ObjectIdsField
from marshmallow import fields
from bson.objectid import ObjectId
from rest_framework.exceptions import ValidationError
from constants.params_validation_type import ParamsValidationType
import os
from utils.array_util import ArrayUtil
from constants.access import SCHOOL_ROLES, HOLDING_ROLES


class BaseSerializer(serializers.Serializer):

    def __new__(cls, *args, **kwargs):
        meta = getattr(cls, "Meta", None)
        if getattr(meta, "many", False) and "many" not in kwargs:
            kwargs["many"] = True
        return super().__new__(cls)

    def __init__(
        self,
        *args,
        service=None,
        method_name=None,
        secret=None,
        model=None,
        user=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.service = service
        self.method_name = method_name
        self.secret = secret
        self.model = model
        self.user = user
        self.validate_model = getattr(getattr(self, "Meta", None), "validate_model", {})

    def validate(self, value):
        extra = {}
        for k, v in self.validate_model.items():
            schema_fields = [
                k for k, v in v.get("model").schema._declared_fields.items()
            ]
            query = {}
            if (
                self.user
                and any(role in self.user.role.split(",") for role in SCHOOL_ROLES)
                and "school_id" in schema_fields
            ):
                query["school_id"] = ObjectId(self.user.school_id)

            if (
                self.user
                and any(role in self.user.role.split(",") for role in HOLDING_ROLES)
                and "holding_id" in schema_fields
            ):
                query["holding_id"] = ObjectId(self.user.holding_id)

            field_value = value.get(k)
            if field_value:
                field_type = ParamsValidationType.OBJECT_ID
                if v.get("type"):
                    field_type = v.get("type")
                if field_type == ParamsValidationType.OBJECT_ID:
                    query[v["field"]] = ObjectId(field_value)
                    result = v["model"].find_one(query)
                    if not result:
                        raise ValidationError(
                            f"{v['model'].collection_name} with ID '{field_value}' not found."
                        )
                elif field_type == ParamsValidationType.STRING:
                    query[v["field"]] = field_value
                    result = v["model"].find_one(query)
                    if not result:
                        raise ValidationError(
                            f"{v['model'].collection_name} with ID '{field_value}' not found."
                        )
                elif field_type == ParamsValidationType.OBJECT_IDS:
                    if not ArrayUtil.is_unique(field_value):
                        raise ValidationError(f"{k} tidak valid.")
                    field_value = [ObjectId(item) for item in field_value]
                    query[v["field"]] = {"$in": field_value}
                    result = {}
                    res = v["model"].find(query)
                    if len(res) != len(field_value):
                        raise ValidationError(f"{k} tidak valid.")
                    result = res
                elif field_type == ParamsValidationType.LIST_STRING:
                    if not ArrayUtil.is_unique(field_value):
                        raise ValidationError(f"{k} tidak valid.")
                    query[v["field"]] = {"$in": field_value}
                    result = {}
                    res = v["model"].find(query)
                    if len(res) != len(field_value):
                        raise ValidationError(f"{k} tidak valid.")
                    result = res
                else:
                    result = {}
                    for i in field_value:
                        result[i] = v["model"].find_one({v["field"]: i})
                extra_key = v["model"].collection_name
                extra[extra_key] = result
                if not extra.get(extra_key):
                    extra[extra_key] = result
                else:
                    extra[f"{extra_key}_{k}"] = result

        function_to_call = getattr(self.service, f"validate_{self.method_name}", None)
        if function_to_call:
            return function_to_call(value, extra, self.secret, self.user)
        return {"value": value, "extra": extra}
