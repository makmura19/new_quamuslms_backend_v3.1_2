from rest_framework.decorators import action
from rest_framework.request import Request

from models.res_user import ResUser
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import LoginSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = ResUser()
    service = MainService()
    data_name = "User"

    actions = {
        "superadmin": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.PUBLIC],
        },
        "login": {
            "method": HTTPMethod.POST,
            "serializer": LoginSerializer,
            "roles": [Role.PUBLIC],
        },
        "change_password": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.ALL],
        },
        "me": {
            "method": HTTPMethod.GET,
            "serializer": None,
            "roles": [Role.ALL],
        },
    }

    params_validation = {}
