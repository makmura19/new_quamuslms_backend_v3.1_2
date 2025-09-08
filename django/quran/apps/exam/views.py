from models.quran_exam import QuranExam
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = QuranExam()
    service = MainService()
    data_name = "QuranExam"

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
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR, Role.TAHFIDZ_COORDINATOR, Role.TAHSIN_COORDINATOR, Role.PRA_TAHSIN_COORDINATOR]
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": UpdateSerializer,
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR, Role.TAHFIDZ_COORDINATOR, Role.TAHSIN_COORDINATOR, Role.PRA_TAHSIN_COORDINATOR]
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR, Role.TAHFIDZ_COORDINATOR, Role.TAHSIN_COORDINATOR, Role.PRA_TAHSIN_COORDINATOR]
        },
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "program_type": ParamsValidationType.STRING,
        "academic_year_id": ParamsValidationType.OBJECT_ID,
        "semester_id": ParamsValidationType.OBJECT_ID
    }
