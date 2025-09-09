from models.lms_exam_type import LmsExamType
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = LmsExamType()
    service = MainService()
    data_name = "LmsExamType"

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
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": UpdateSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
    }

    params_validation = {
        "is_template": ParamsValidationType.BOOLEAN,
        "is_report": ParamsValidationType.BOOLEAN,
        "is_final": ParamsValidationType.BOOLEAN,
        "is_odd_semester": ParamsValidationType.BOOLEAN,
        "is_even_semester": ParamsValidationType.BOOLEAN,
    }
