from helpers.base_viewset import BaseViewSet
from constants.access import Role, Action

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    create_serializer = CreateSerializer
    update_serializer = CreateSerializer
    service = MainService()
    data_name = "File"
    def_list = {
        Action.CREATE: ["__public__"],
    }
    params_validation = {}
