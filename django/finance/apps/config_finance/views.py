from models.config_finance import ConfigFinance
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = ConfigFinance()
    service = MainService()
    data_name = "ConfigFinance"

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
            "roles": [Role.SUPERADMIN, Role.FINANCE],
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": CreateSerializer,
            "roles": [Role.SUPERADMIN, Role.FINANCE],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.FINANCE],
        },
    }

    params_validation = {
        "holding_id": ParamsValidationType.OBJECT_ID,
        "school_id": ParamsValidationType.OBJECT_ID,
        "is_auto_debit": ParamsValidationType.BOOLEAN,
        "is_pocket_auto_debit": ParamsValidationType.BOOLEAN,
        "is_prefix_lock": ParamsValidationType.BOOLEAN,
        "is_active": ParamsValidationType.BOOLEAN,
        "is_active": ParamsValidationType.BOOLEAN,
    }
