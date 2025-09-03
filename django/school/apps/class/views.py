from models.school_class import SchoolClass
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer, UpdateSubjectSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = SchoolClass()
    service = MainService()
    data_name = "SchoolClass"

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
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": UpdateSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "subject": {
            "detail": True,
            "method": HTTPMethod.GET,
            "serializer": None,
            "roles": [Role.ALL],
        },
        "update_subject": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": UpdateSubjectSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
    }

    params_validation = {
        "name": ParamsValidationType.STRING,
        "school_id": ParamsValidationType.OBJECT_ID,
        "academic_year_id": ParamsValidationType.OBJECT_ID,
        "level_id": ParamsValidationType.OBJECT_ID,
        "is_active": ParamsValidationType.BOOLEAN,
    }
