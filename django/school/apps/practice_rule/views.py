from models.mutabaah_practice_rule import MutabaahPracticeRule
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = MutabaahPracticeRule()
    service = MainService()
    data_name = "MutabaahPracticeRule"

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
        # "destroy": {
        #     "method": HTTPMethod.DELETE,
        #     "serializer": None,
        #     "roles": [Role.SUPERADMIN],
        # },
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "level_id": ParamsValidationType.OBJECT_ID,
        "days_of_week": ParamsValidationType.INT,
        "period": ParamsValidationType.STRING,
        "submitted_by": ParamsValidationType.STRING,
        "is_active": ParamsValidationType.BOOLEAN,
    }
