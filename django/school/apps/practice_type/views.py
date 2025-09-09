from models.mutabaah_practice_type import MutabaahPracticeType
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = MutabaahPracticeType()
    service = MainService()
    data_name = "MutabaahPracticeType"

    actions = {
        "list": {
            "method": HTTPMethod.GET,
            "serializer": None,
            "roles": [Role.ALL],
        },
        "retrieve": {
            "method": HTTPMethod.GET,
            "serializer": None,
            "roles": [Role.ALL],
        },
        "create": {
            "method": HTTPMethod.POST,
            "serializer": CreateSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": UpdateSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "type": ParamsValidationType.STRING,
        "period": ParamsValidationType.STRING,
        "gender": ParamsValidationType.STRING,
        "weight_formula": ParamsValidationType.STRING,
        "mandatory_type": ParamsValidationType.STRING,
        "submitted_by": ParamsValidationType.STRING,
        "has_day_count": ParamsValidationType.BOOLEAN,
        "is_template": ParamsValidationType.BOOLEAN,
    }
