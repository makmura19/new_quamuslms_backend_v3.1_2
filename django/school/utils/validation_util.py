from rest_framework.exceptions import ValidationError


class ValidationUtil:
    @staticmethod
    def validate_required_fields(data: dict, required_fields: list):
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValidationError(f"Missing required fields: {', '.join(missing)}")

    @staticmethod
    def clean_data_against_schema(data: dict, schema_fields: dict):
        return {k: v for k, v in data.items() if k in schema_fields}
