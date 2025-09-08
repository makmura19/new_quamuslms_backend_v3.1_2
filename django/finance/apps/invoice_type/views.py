from models.finance_invoice_type import FinanceInvoiceType
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer, ImportXlsxSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = FinanceInvoiceType()
    service = MainService()
    data_name = "FinanceInvoiceType"

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
            "serializer": UpdateSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_FINANCE, Role.FINANCE],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.HOLDING_FINANCE, Role.FINANCE],
        },
        "import_xlsx": {
            "method": HTTPMethod.POST,
            "serializer": ImportXlsxSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_FINANCE, Role.FINANCE],
        },
        
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "type": ParamsValidationType.STRING,
        "is_male": ParamsValidationType.BOOLEAN,
        "is_female": ParamsValidationType.BOOLEAN,
        "is_installment": ParamsValidationType.BOOLEAN,
        "is_active": ParamsValidationType.BOOLEAN,
    }
