from bson import ObjectId
from constants.params_validation_type import ParamsValidationType


class IDUtil:
    @staticmethod
    def parse(value, type_id):
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
