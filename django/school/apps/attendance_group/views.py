from models.tap_attendance_group import TapAttendanceGroup
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = TapAttendanceGroup()
    service = MainService()
    data_name = "TapAttendanceGroup"

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
            "serializer": UpdateSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "activate": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "for_student": ParamsValidationType.BOOLEAN,
        "for_teacher": ParamsValidationType.BOOLEAN,
        "teacher_ids": ParamsValidationType.OBJECT_ID,
        "is_all_teacher": ParamsValidationType.BOOLEAN,
        "is_default": ParamsValidationType.BOOLEAN,
        "is_active": ParamsValidationType.BOOLEAN,
    }
