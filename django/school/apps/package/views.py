from models.cbt_package import CbtPackage
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = CbtPackage()
    service = MainService()
    data_name = "CbtPackage"

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
            "roles": [Role.TEACHER],
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": CreateSerializer,
            "roles": [Role.TEACHER],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.TEACHER],
        },
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "teacher_id": ParamsValidationType.OBJECT_ID,
        "subject_id": ParamsValidationType.OBJECT_ID,
        "level_id": ParamsValidationType.OBJECT_ID,
        "is_public": ParamsValidationType.BOOLEAN,
        "is_active": ParamsValidationType.BOOLEAN,
    }
