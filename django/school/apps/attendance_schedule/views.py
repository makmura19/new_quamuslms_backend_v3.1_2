from models.tap_attendance_schedule import TapAttendanceSchedule
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = TapAttendanceSchedule()
    service = MainService()
    data_name = "TapAttendanceSchedule"

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
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "group_id": ParamsValidationType.OBJECT_ID,
        "level_id": ParamsValidationType.OBJECT_ID,
        "day": ParamsValidationType.STRING,
        "for_student": ParamsValidationType.BOOLEAN,
        "for_teacher": ParamsValidationType.BOOLEAN,
        "is_active": ParamsValidationType.BOOLEAN,
    }
