from models.cbt_question import CbtQuestion
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = CbtQuestion()
    service = MainService()
    data_name = "CbtQuestion"

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
            "roles": [Role.TEACHER],
        },
        "update": {
            "method": HTTPMethod.PUT,
            "serializer": UpdateSerializer,
            "roles": [Role.TEACHER],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.TEACHER],
        },
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "teacher_id": ParamsValidationType.OBJECT_ID,
        "type_id": ParamsValidationType.OBJECT_ID,
        "school_subject_id": ParamsValidationType.OBJECT_ID,
        "edu_subject_id": ParamsValidationType.OBJECT_ID,
        "level_id": ParamsValidationType.OBJECT_ID,
        "chapter_id": ParamsValidationType.OBJECT_ID,
        "difficulty": ParamsValidationType.STRING,
        "is_public": ParamsValidationType.BOOLEAN,
        "is_active": ParamsValidationType.BOOLEAN,
    }
