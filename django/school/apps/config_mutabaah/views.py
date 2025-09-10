from models.config_mutabaah import ConfigMutabaah
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import UpdateMeSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = ConfigMutabaah()
    service = MainService()
    data_name = "ConfigMutabaah"

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
