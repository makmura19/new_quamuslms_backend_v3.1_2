from models.school_student import SchoolStudent
from helpers.base_viewset import BaseViewSet
from constants.access import Role
from constants.params_validation_type import ParamsValidationType
from constants.http_method import HTTPMethod

from .serializers import (
    CreateSerializer,
    UpdateSerializer,
    InputXlsSerializer,
    UploadPhotoSerializer,
    ImportUpdateSerializer,
    ActivateSerializer,
    UpdatePinSerializer,
    ClassSerializer
) 
from .service import MainService


class MainViewSet(BaseViewSet):
    model = SchoolStudent()
    service = MainService()
    data_name = "SchoolStudent"

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
        "upload_photo": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": UploadPhotoSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "input_xls": {
            "detail": False,
            "method": HTTPMethod.POST,
            "serializer": InputXlsSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "export_update": {
            "method": HTTPMethod.GET,
            "serializer": None,
            "roles": [Role.ALL],
        },
        "import_update": {
            "detail": False,
            "method": HTTPMethod.POST,
            "serializer": ImportUpdateSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "account": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": None,
            "roles": [Role.SUPERADMIN],
        },
        "activate": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": ActivateSerializer,
            "roles": [Role.SUPERADMIN],
        },
        "update_pin": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": UpdatePinSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "move_class": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": ClassSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        "class_": {
            "detail": True,
            "method": HTTPMethod.PUT,
            "serializer": ClassSerializer,
            "roles": [Role.SUPERADMIN, Role.HOLDING_ADMIN, Role.ADMINISTRATOR],
        },
        
    }

    params_validation = {
        "school_id": ParamsValidationType.OBJECT_ID,
        "gender": ParamsValidationType.STRING,
        "class_id": ParamsValidationType.OBJECT_ID,
        "level_id": ParamsValidationType.OBJECT_ID,
        "class_academic_year_id": ParamsValidationType.OBJECT_ID,
        "class_history_ids": ParamsValidationType.OBJECT_ID,
        "join_academic_year_id": ParamsValidationType.OBJECT_ID,
        "program_id": ParamsValidationType.OBJECT_ID,
        "major_id": ParamsValidationType.OBJECT_ID,
        "degree_id": ParamsValidationType.OBJECT_ID,
        "stage_group_id": ParamsValidationType.OBJECT_ID,
        "stage_id": ParamsValidationType.OBJECT_ID,
        "quran_class_ids": ParamsValidationType.OBJECT_ID,
        "dormitory_room_id": ParamsValidationType.OBJECT_ID,
        "is_alumni": ParamsValidationType.BOOLEAN,
        "is_boarding": ParamsValidationType.BOOLEAN,
        "is_active": ParamsValidationType.BOOLEAN,
    }
