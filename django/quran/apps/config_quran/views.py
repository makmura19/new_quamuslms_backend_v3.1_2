from models.config_quran import ConfigQuran
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import UpdateMeSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = ConfigQuran()
    service = MainService()
    data_name = "ConfigQuran"

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

    params_validation = {
        "school_id":ParamsValidationType.OBJECT_ID
    }
