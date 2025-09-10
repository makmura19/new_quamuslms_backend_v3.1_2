from models.psb_psb import PsbPsb
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = PsbPsb()
    service = MainService()
    data_name = "PsbPsb"

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
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.HOLDING_STAFF, Role.ADMINISTRATOR],
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": CreateSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.HOLDING_STAFF, Role.ADMINISTRATOR],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.HOLDING_STAFF, Role.ADMINISTRATOR]
        },
    }

    params_validation = {
        "holding_id": ParamsValidationType.OBJECT_ID,
        "school_id": ParamsValidationType.OBJECT_ID,
        "is_active": ParamsValidationType.BOOLEAN
    }
