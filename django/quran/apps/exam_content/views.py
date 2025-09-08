from models.quran_exam_content import QuranExamContent
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, SequenceSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = QuranExamContent()
    service = MainService()
    data_name = "QuranExamContent"

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
        "sequence": {
            "method": HTTPMethod.POST,
            "serializer": SequenceSerializer,
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR, Role.TAHFIDZ_COORDINATOR, Role.TAHSIN_COORDINATOR, Role.PRA_TAHSIN_COORDINATOR]
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": CreateSerializer,
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
        "exam_id": ParamsValidationType.OBJECT_ID,
        "juz": ParamsValidationType.STRING
    }
