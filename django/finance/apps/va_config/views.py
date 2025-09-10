from models.finance_va_config import FinanceVaConfig
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = FinanceVaConfig()
    service = MainService()
    data_name = "FinanceVaConfig"

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
            "roles": [Role.SUPERADMIN, Role.STAFF_ADMIN],
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": CreateSerializer,
            "roles": [Role.SUPERADMIN, Role.STAFF_ADMIN],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.STAFF_ADMIN],
        },
    }

    params_validation = {
        "bank_id": ParamsValidationType.OBJECT_ID,
        "vendor_id": ParamsValidationType.OBJECT_ID,
        "holding_id": ParamsValidationType.OBJECT_ID,
        "school_id": ParamsValidationType.OBJECT_ID,
    }
