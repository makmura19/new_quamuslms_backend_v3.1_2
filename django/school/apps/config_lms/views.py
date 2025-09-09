from models.config_lms import ConfigLms
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import UpdateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = ConfigLms()
    service = MainService()
    data_name = "ConfigLms"

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
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": UpdateSerializer,
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR],
        },
        "me": {
            "detail": False,
            "method": HTTPMethod.GET,
            "serializer": None,
            "roles": [Role.ADMINISTRATOR],
        },
        "update_me": {
            "detail": False,
            "method": HTTPMethod.POST,
            "serializer": UpdateSerializer,
            "roles": [Role.ADMINISTRATOR],
        },
    }

    params_validation = {
        "school_id__req": ParamsValidationType.OBJECT_ID
    }
