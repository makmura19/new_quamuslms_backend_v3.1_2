from models.res_bank import ResBank
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UploadImageSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = ResBank()
    service = MainService()
    data_name = "ResBank"

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
            "serializer": CreateSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "upload_image": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": UploadImageSerializer,
            "roles": [Role.SUPERADMIN],
        },
    }

    params_validation = {
        "name": ParamsValidationType.STRING,
        "short_name": ParamsValidationType.STRING,
        "is_active": ParamsValidationType.BOOLEAN,
    }
