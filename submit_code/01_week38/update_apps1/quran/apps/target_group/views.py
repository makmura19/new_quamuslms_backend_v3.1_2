from models.quran_target_group import QuranTargetGroup
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = QuranTargetGroup()
    service = MainService()
    data_name = "QuranTargetGroup"

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
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR],
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": CreateSerializer,
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR],
        },
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "program_type": ParamsValidationType.STRING,
        "is_active": ParamsValidationType.BOOLEAN
    }
