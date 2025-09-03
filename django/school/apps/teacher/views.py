from models.school_teacher import SchoolTeacher
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer, InputXlsSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = SchoolTeacher()
    service = MainService()
    data_name = "SchoolTeacher"

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
        "input_xls": {
            "method": HTTPMethod.POST,
            "serializer": InputXlsSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": UpdateSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "account": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "name": ParamsValidationType.STRING,
        "login": ParamsValidationType.STRING,
        "staff_no": ParamsValidationType.STRING,
        "resident_no": ParamsValidationType.STRING,
        "is_active": ParamsValidationType.BOOLEAN,
    }
