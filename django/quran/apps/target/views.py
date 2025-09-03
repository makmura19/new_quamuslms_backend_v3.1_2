from models.quran_target import QuranTarget
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, SequenceSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = QuranTarget()
    service = MainService()
    data_name = "QuranTarget"

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
        "sequence": {
            "method": HTTPMethod.POST,
            "serializer": SequenceSerializer,
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
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR]
        },
    }

    params_validation = {
        "group_id": ParamsValidationType.OBJECT_ID,
        "class_id": ParamsValidationType.OBJECT_ID,
        "school_id": ParamsValidationType.OBJECT_ID,
        "program_type": ParamsValidationType.STRING,
        "tahfidz_type": ParamsValidationType.STRING,
        "method_id": ParamsValidationType.OBJECT_ID,
        "book_id": ParamsValidationType.OBJECT_ID
    }
