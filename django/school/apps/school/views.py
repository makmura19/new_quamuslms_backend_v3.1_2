from models.school_school import SchoolSchool
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import (
    CreateSerializer,
    UpdateSerializer,
    ActivateSerializer,
    UploadLogoSerializer,
    ModuleSerializer,
)
from .service import MainService


class MainViewSet(BaseViewSet):
    model = SchoolSchool()
    service = MainService()
    data_name = "SchoolSchool"

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
            "serializer": UpdateSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "activate": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": ActivateSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "account": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": UpdateSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "module": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": ModuleSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "teacher_account": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "student_account": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "upload_logo": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": UploadLogoSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "level": {
            "detail": True,
            "method": HTTPMethod.GET,
            "serializer": None,
            "roles": [Role.ALL],
        },
    }

    params_validation = {
        "code": ParamsValidationType.STRING,
        "name": ParamsValidationType.STRING,
        "display_name": ParamsValidationType.STRING,
        "npsn": ParamsValidationType.STRING,
        "module_codes": ParamsValidationType.STRING,
        "group_ids": ParamsValidationType.OBJECT_ID,
        "is_active": ParamsValidationType.BOOLEAN,
        "is_school": ParamsValidationType.BOOLEAN,
        "is_holding": ParamsValidationType.BOOLEAN,
    }
