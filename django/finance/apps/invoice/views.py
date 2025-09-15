from models.finance_invoice import FinanceInvoice
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = FinanceInvoice()
    service = MainService()
    data_name = "FinanceInvoice"

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
        "student": {
            "detail": False,
            "method": HTTPMethod.GET,
            "serializer": CreateSerializer,
            "roles": [Role.ALL],
        },
    }

    params_validation = {
        "holding_id": ParamsValidationType.OBJECT_ID,
        "school_id": ParamsValidationType.OBJECT_ID,
        "academic_year_id": ParamsValidationType.OBJECT_ID,
        "semester": ParamsValidationType.INT,
        "year": ParamsValidationType.INT,
        "month": ParamsValidationType.INT,
        "student_id": ParamsValidationType.OBJECT_ID,
        "type_id": ParamsValidationType.OBJECT_ID,
        "type": ParamsValidationType.STRING,
        "is_installment": ParamsValidationType.BOOLEAN,
        "status": ParamsValidationType.STRING,
        "is_paid_off": ParamsValidationType.BOOLEAN,
        "class_id": ParamsValidationType.OBJECT_ID,
    }