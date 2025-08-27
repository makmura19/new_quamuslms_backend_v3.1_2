from bson import ObjectId
import inspect
from marshmallow import fields as ma_fields
from helpers.custom_model_field import ObjectIdField
from enum import Enum
from constants.params_validation_type import ParamsValidationType
from bson import ObjectId
from typing import get_args, get_origin, Optional, Union


class DictUtil:
    @staticmethod
    def parse_id_by_type(value, type_id):
        if value is None:
            return None

        if type_id == ParamsValidationType.OBJECT_ID:
            try:
                return ObjectId(value)
            except Exception:
                raise ValueError("Invalid ObjectId format")

        elif type_id == ParamsValidationType.INT:
            try:
                return int(value)
            except ValueError:
                raise ValueError("Invalid integer ID format")

        elif type_id == ParamsValidationType.STRING:
            return str(value)

        raise ValueError(f"Unknown type_id: {type_id}")

    # @staticmethod
    # def get_id_type_from_dataclass(cls) -> ParamsValidationType:
    #     id_field = cls.__dataclass_fields__.get("_id")
    #     if not id_field:
    #         return ParamsValidationType.UNKNOWN

    #     marshmallow_field = id_field.metadata.get("marshmallow_field")

    #     if isinstance(marshmallow_field, ObjectIdField):
    #         return ParamsValidationType.OBJECT_ID
    #     elif isinstance(marshmallow_field, ma_fields.String):
    #         return ParamsValidationType.STRING
    #     elif isinstance(marshmallow_field, ma_fields.Integer):
    #         return ParamsValidationType.INT
    #     else:
    #         return ParamsValidationType.UNKNOWN

    @staticmethod
    def get_id_type_from_dataclass(cls) -> ParamsValidationType:
        id_field = cls.__dataclass_fields__.get("_id")
        if not id_field:
            return ParamsValidationType.UNKNOWN

        id_type = id_field.type

        if get_origin(id_type) is Optional or get_origin(id_type) is Union:
            args = get_args(id_type)
            if ObjectId in args:
                return ParamsValidationType.OBJECT_ID
            elif str in args:
                return ParamsValidationType.STRING
            elif int in args:
                return ParamsValidationType.INT
        else:
            if id_type == ObjectId:
                return ParamsValidationType.OBJECT_ID
            elif id_type == str:
                return ParamsValidationType.STRING
            elif id_type == int:
                return ParamsValidationType.INT

        return ParamsValidationType.UNKNOWN

    @staticmethod
    def filter_dataclass_fields(cls, data: dict):
        valid_fields = {f.name for f in inspect.signature(cls).parameters.values()}
        return {k: v for k, v in data.items() if k in valid_fields}

    @staticmethod
    def remove_key(data, keys_to_remove):
        if isinstance(keys_to_remove, str):
            keys_to_remove = [keys_to_remove]
        elif not isinstance(keys_to_remove, list):
            raise ValueError("keys_to_remove harus berupa string atau list of strings.")

        if not all(isinstance(key, str) for key in keys_to_remove):
            raise ValueError("Semua elemen dalam keys_to_remove harus berupa string.")

        return {k: v for k, v in data.items() if k not in keys_to_remove}

    @staticmethod
    def find_by_key(data, target_key):
        if target_key in data:
            return data[target_key]
        for key, value in data.items():
            if isinstance(value, dict):
                result = DictUtil.find_by_key(value, target_key)
                if result is not None:
                    return result
        return None

    @staticmethod
    def remove_duplicates(data):
        seen_values = set()
        result = {}
        for key, value in data.items():
            if value not in seen_values:
                result[key] = value
                seen_values.add(value)
        return result

    @staticmethod
    def flatten_dict(data, parent_key="", sep="."):
        items = []
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(DictUtil.flatten_dict(value, new_key, sep=sep).items())
            else:
                items.append((new_key, value))
        return dict(items)

    @staticmethod
    def merge_dicts(*dicts):
        merged = {}
        for d in dicts:
            if d:
                merged.update(d)
        return merged

    @staticmethod
    def filter_keys(data: dict, allowed_keys: list):
        return {k: v for k, v in data.items() if k in allowed_keys}

    @staticmethod
    def exclude_keys(data: dict, excluded_keys: list):
        return {k: v for k, v in data.items() if k not in excluded_keys}

    @staticmethod
    def invert_dict(data):
        return {v: k for k, v in data.items()}

    @staticmethod
    def validate_dict(data, validation):
        validated_data = {}

        for key, value in data.items():
            if key in validation:
                try:
                    if validation[key] == ObjectId:
                        try:
                            ObjectId(value)
                            validated_data[key] = f"oid_{value}"
                        except Exception:
                            raise ValueError(
                                f"Invalid ObjectId string for key '{key}': {value}"
                            )
                    elif validation[key] == bool:
                        if int(value) not in [0, 1]:
                            raise ValueError(f"Validation failed for key '{key}': {e}")
                        validated_data[key] = True if int(value) == 1 else False
                    else:
                        validated_data[key] = validation[key](value)
                except Exception as e:
                    raise ValueError(f"Validation failed for key '{key}': {e}")

        return validated_data

    @staticmethod
    def replace_new_ids(obj, isObjectId=True):
        if isinstance(obj, dict):
            new_obj = {}
            for k, v in obj.items():
                new_obj["is_new"] = False
                if k == "_id":
                    if isinstance(v, str) and v.startswith("new_"):
                        new_obj["is_new"] = True
                        new_obj[k] = ObjectId() if isObjectId else str(ObjectId())
                    elif isObjectId and not isinstance(v, ObjectId):
                        try:
                            new_obj[k] = ObjectId(v)
                        except Exception:
                            new_obj[k] = v
                    else:
                        new_obj[k] = v
                else:
                    new_obj[k] = DictUtil.replace_new_ids(v, isObjectId)
            return new_obj
        elif isinstance(obj, list):
            return [DictUtil.replace_new_ids(i, isObjectId) for i in obj]
        else:
            return obj

    def add_ownership(user, query_params, params_validation, key="company_id"):
        company_id = user.company_id
        query_params = {**query_params, "company_id": company_id}
        params_validation = {
            **params_validation,
            "company_id": ParamsValidationType.OBJECT_ID,
        }
        return query_params, params_validation
