from models.finance_invoice_price_variant import FinanceInvoicePriceVariant
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = FinanceInvoicePriceVariant()
    service = MainService()
    data_name = "FinanceInvoicePriceVariant"

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
            "roles": [Role.SUPERADMIN, Role.HOLDING_FINANCE, Role.FINANCE, Role.ADMINISTRATOR],
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
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "price_id": ParamsValidationType.OBJECT_ID,
        "type_id": ParamsValidationType.OBJECT_ID,
        "is_active": ParamsValidationType.BOOLEAN,
    }
