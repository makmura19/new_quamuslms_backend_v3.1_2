from models.quran_report_type import QuranReportType
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import CreateSerializer, UploadPreviewSerializer
from .service import MainService


class MainViewSet(BaseViewSet):
    model = QuranReportType()
    service = MainService()
    data_name = "QuranReportType"

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
            "serializer": CreateSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "destroy": {
            "method": HTTPMethod.DELETE,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "upload_preview": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": UploadPreviewSerializer,
            "roles": [Role.SUPERADMIN],
        },
    }

    params_validation = {
        "program_type": ParamsValidationType.STRING
    }
