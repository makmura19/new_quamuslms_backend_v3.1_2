from models.quran_score_option import QuranScoreOption
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = QuranScoreOption()
    service = MainService()
    data_name = "QuranScoreOption"

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
            "serializer": UpdateSerializer,
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN, Role.ADMINISTRATOR],
        },
    }

    params_validation = {
        "category_id": ParamsValidationType.OBJECT_ID,
        "type_id": ParamsValidationType.OBJECT_ID,
        "is_penalty": ParamsValidationType.BOOLEAN,
        "under_category": ParamsValidationType.BOOLEAN,
        "use_parent_score": ParamsValidationType.BOOLEAN
    }
