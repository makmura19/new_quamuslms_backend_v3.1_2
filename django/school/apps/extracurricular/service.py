from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError


class MainService(BaseService):
    
    @staticmethod
    def list(
        model: BaseModel, query_params, params_validation, user, headers_dict=None
    ):
        result = model.aggregate(
            add_metadata=True,
            query_params=query_params,
            params_validation=params_validation,
            fields=query_params.get("fields"),
            exclude=query_params.get("exclude"),
            lookup=["school","teachers"]
        )
        return result
