from models.res_bank import ResBank
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .service import MainService


class MainViewSet(BaseViewSet):
    model = ResBank()
    service = MainService()
    data_name = "ResBank"

    actions = {
        "academic_year": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "subject": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "stage": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "stage_level": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "stage_group": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "subject_level": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "quran_chapter": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "quran_juz": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "quran_page": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "quran_line": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "quran_verse": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "quran_word": {
            "method": HTTPMethod.POST,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
    }

    params_validation = {}
