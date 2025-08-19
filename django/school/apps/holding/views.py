from models.school_holding import SchoolHolding
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UploadLogoSerializer, StaffSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = SchoolHolding()
    service = MainService()
    data_name = "SchoolHolding"

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
        "upload_logo": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": UploadLogoSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "staff": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": StaffSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
    }

    params_validation = {
        "name": ParamsValidationType.STRING,
        "display_name": ParamsValidationType.STRING,
        "module_codes": ParamsValidationType.STRING,
        "is_active": ParamsValidationType.BOOLEAN,
    }
