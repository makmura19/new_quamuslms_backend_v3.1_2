from models.config_lms import ConfigLms
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import UpdateMeSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = ConfigLms()
    service = MainService()
    data_name = "ConfigLms"

    actions = {
        "retrieve": {
            "method": HTTPMethod.GET,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR],
        },
        "update": {
            "method": HTTPMethod.POST,
            "serializer": UpdateMeSerializer,
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR],
        },
    }

    params_validation = {}
