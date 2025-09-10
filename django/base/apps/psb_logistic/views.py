from models.psb_logistic import PsbLogistic
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = PsbLogistic()
    service = MainService()
    data_name = "PsbLogistic"

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
            "serializer": CreateSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
    }

    params_validation = {
        "holding_id": ParamsValidationType.OBJECT_ID,
        "school_id": ParamsValidationType.OBJECT_ID,
        "psb_id": ParamsValidationType.OBJECT_ID,
        "gender": ParamsValidationType.STRING,
        "boarding": ParamsValidationType.STRING
    }
