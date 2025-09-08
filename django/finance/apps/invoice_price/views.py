from models.finance_invoice_price import FinanceInvoicePrice
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = FinanceInvoicePrice()
    service = MainService()
    data_name = "FinanceInvoicePrice"
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
            "roles": [Role.SUPERADMIN, Role.HOLDING_FINANCE, Role.FINANCE],
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": CreateSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_FINANCE, Role.FINANCE],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.HOLDING_FINANCE, Role.FINANCE],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "type_id": ParamsValidationType.OBJECT_ID,
        "level_id": ParamsValidationType.OBJECT_ID,
        "is_active": ParamsValidationType.BOOLEAN,
    }
