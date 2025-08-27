from models.school_subject import SchoolSubject
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UpdateSerializer, UploadImageSerializer, SequenceSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = SchoolSubject()
    service = MainService()
    data_name = "SchoolSubject"

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
        "upload_img": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": UploadImageSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "sequence": {
            "method": HTTPMethod.POST,
            "serializer": SequenceSerializer,
            "roles": [Role.SUPERADMIN],
        },
    }

    params_validation = {
        "name": ParamsValidationType.STRING,
        "short_name": ParamsValidationType.STRING,
        "school_id": ParamsValidationType.OBJECT_ID,
        "subject_id": ParamsValidationType.OBJECT_ID,
    }
