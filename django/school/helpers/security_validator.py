from typing import Dict, List, Optional
from marshmallow.validate import OneOf
from rest_framework.exceptions import ValidationError
from datetime import datetime
import importlib
from marshmallow import ValidationError
from dataclasses import asdict


class SecurityValidator:
    IMMUTABLE_FIELDS = ["_id", "created_at", "is_deleted", "deleted_at"]

    @staticmethod
    def remove_immutable_fields(data: Dict) -> Dict:
        return {
            k: v for k, v in data.items() if k not in SecurityValidator.IMMUTABLE_FIELDS
        }

    @staticmethod
    def filter_whitelist_fields(
        data: Dict, whitelist: Optional[List[str]] = None
    ) -> Dict:
        if whitelist is None:
            return data
        return {k: v for k, v in data.items() if k in whitelist}

    @staticmethod
    def validate_enum_fields(data: Dict, schema) -> None:
        errors = {}
        for key, value in data.items():
            field = schema.fields.get(key)
            if field and hasattr(field, "validate"):
                validators = field.validate
                if not isinstance(validators, (list, tuple)):
                    validators = [validators]

                for validator in validators:
                    if isinstance(validator, OneOf):
                        if value not in validator.choices:
                            errors[key] = (
                                f"'{value}' bukan pilihan yang valid. Pilih salah satu dari {validator.choices}"
                            )
        if errors:
            raise ValidationError(errors)

    @staticmethod
    def secure_update(
        data: Dict, schema=None, whitelist: Optional[List[str]] = None
    ) -> Dict:
        data = SecurityValidator.remove_immutable_fields(data)
        if whitelist:
            data = SecurityValidator.filter_whitelist_fields(data, whitelist)
        if schema:
            SecurityValidator.validate_enum_fields(data, schema)
        data["updated_at"] = datetime.utcnow()
        return data

    @staticmethod
    def validate_data(*datas):
        validated_data = []

        for data in datas:
            if isinstance(data, list):
                for item in data:
                    SecurityValidator._validate_single_data(item, validated_data)
            else:
                SecurityValidator._validate_single_data(data, validated_data)

        return True

    @staticmethod
    def _validate_single_data(data, validated_data):
        cls_name = data.__class__.__name__

        if not cls_name.endswith("Data"):
            raise ValueError(
                f"Data class '{cls_name}' tidak valid, harus berakhiran 'Data'"
            )

        schema_class_name = cls_name.replace("Data", "Schema")
        module_name = SecurityValidator._resolve_module_from_class_name(cls_name)

        try:
            mod = importlib.import_module(module_name)
            schema_class = getattr(mod, schema_class_name)
        except (ModuleNotFoundError, AttributeError):
            raise ImportError(
                f"Tidak bisa mengimport {schema_class_name} dari {module_name}"
            )

        schema = schema_class()

        try:
            schema.load(asdict(data))
            validated_data.append(True)
        except ValidationError as e:
            raise ValidationError({cls_name: e.messages})

    @staticmethod
    def _resolve_module_from_class_name(class_name):
        base_name = class_name.replace("Data", "")
        return f"models.{SecurityValidator.camel_to_snake(base_name)}"

    @staticmethod
    def camel_to_snake(name):
        import re

        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
