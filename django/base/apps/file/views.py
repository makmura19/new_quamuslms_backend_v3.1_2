from models.res_file import ResFile
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = ResFile()
    service = MainService()
    data_name = "ResFile"

    actions = {
        "create": {
            "method": HTTPMethod.POST,
            "serializer": CreateSerializer,
            "roles": [Role.PUBLIC],
        },
    }

    params_validation = {}
