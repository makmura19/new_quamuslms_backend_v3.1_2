from marshmallow import fields, ValidationError
from bson import ObjectId
from datetime import datetime, date
from dateutil.parser import isoparse


class ObjectIdField(fields.Field):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("allow_none", True)
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        if isinstance(value, ObjectId):
            return value
        if isinstance(value, str):
            try:
                return ObjectId(value)
            except Exception:
                raise ValidationError("Invalid ObjectId string.")
        raise ValidationError("Must be a valid ObjectId or its string representation.")


class ObjectIdsField(fields.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if not value:
            return []
        return [str(v) for v in value]

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return []
        if not isinstance(value, list):
            raise ValidationError("Must be a list of valid ObjectId.")
        result = []
        for i in value:
            try:
                result.append(ObjectId(i) if isinstance(i, str) else i)
            except Exception:
                raise ValidationError("Invalid ObjectId string in list.")
        return result


class AnyField(fields.Field):
    def __init__(self, allowed_types=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_types = allowed_types or []

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        if not self.allowed_types:
            return value
        for allowed_type in self.allowed_types:
            if isinstance(value, allowed_type):
                return value
        allowed_type_names = [t.__name__ for t in self.allowed_types]
        raise ValidationError(
            f"Invalid type. Expected one of: {', '.join(allowed_type_names)}."
        )


from marshmallow import ValidationError, fields
from datetime import datetime, date


class DateField(fields.Field):
    def __init__(self, allow_null=False, **kwargs):
        self.allow_null = allow_null
        kwargs["allow_none"] = allow_null
        super().__init__(**kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None and self.allow_null:
            return None
        if not isinstance(value, (datetime, date)):
            raise ValidationError("Value must be a valid date or datetime object.")
        return value.isoformat()[:10]

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None and self.allow_null:
            return None
        if not value:
            raise ValidationError("This field is required unless allow_null=True.")
        try:
            if isinstance(value, datetime):
                return datetime(value.year, value.month, value.day)
            if isinstance(value, date):
                return datetime(value.year, value.month, value.day)
            if isinstance(value, str):
                date_obj = datetime.strptime(value, "%Y-%m-%d")
                return datetime(date_obj.year, date_obj.month, date_obj.day)
            raise ValidationError("Invalid input type for DateField.")
        except Exception:
            raise ValidationError("Invalid date format. Expected YYYY-MM-DD")


class DateTimeField(fields.Field):
    def __init__(self, allow_null=False, **kwargs):
        self.allow_null = allow_null
        kwargs["allow_none"] = allow_null
        super().__init__(**kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None and self.allow_null:
            return None
        if not isinstance(value, datetime):
            raise ValidationError("Value must be a valid datetime object.")
        return value.isoformat()

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None and self.allow_null:
            return None
        if isinstance(value, datetime):
            return value
        if not isinstance(value, str):
            raise ValidationError("Datetime must be a string in ISO format.")
        try:
            return isoparse(value)
        except Exception:
            raise ValidationError("Invalid datetime format. Expected ISO 8601 format.")
