from models.quran_class import QuranClass
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = QuranClass()
    service = MainService()
    data_name = "QuranClass"

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
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "is_active": ParamsValidationType.BOOLEAN,
        "program_type": ParamsValidationType.STRING,
        "academic_year_id": ParamsValidationType.OBJECT_ID,
        "teacher_id": ParamsValidationType.OBJECT_ID,
        "teacher_ids": ParamsValidationType.OBJECT_IDS,
        "type": ParamsValidationType.STRING,
        "target_type": ParamsValidationType.STRING
    }
