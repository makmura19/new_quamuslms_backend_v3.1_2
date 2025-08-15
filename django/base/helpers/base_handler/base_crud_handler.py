from utils.json_util import JsonUtil
from utils.response_handler import ResponseHandler
from utils.error_handler import ErrorHandler
from rest_framework.exceptions import ValidationError
from helpers.base_handler.base_object_util import BaseObjectUtil
import os
from constants.access import SCHOOL_ROLES, HOLDING_ROLES


class BaseCRUDHandler:
    @staticmethod
    def inject_company_id(data: dict, user) -> dict:
        if (
            user
            and user.is_authenticated
            and any(role in user.role.split(",") for role in SCHOOL_ROLES)
        ):
            data["school_id"] = user.school_id

        if (
            user
            and user.is_authenticated
            and any(role in user.role.split(",") for role in HOLDING_ROLES)
        ):
            data["holding_id"] = user.holding_id
        return data

    @staticmethod
    def create(method_name, request, serializer, model, service, data_name):
        try:
            file_data = {
                field: (
                    request.FILES.getlist(field)[0]
                    if len(request.FILES.getlist(field)) == 1
                    else request.FILES.getlist(field)
                )
                for field in request.FILES
            }

            data = {**request.data, **file_data}
            form_data = request.data.get("form_data")
            if form_data:
                data.update(JsonUtil.smart_json_loads(form_data))

            BaseCRUDHandler.inject_company_id(data, request.user)

            secret = request.META.get("HTTP_X_SECRET")
            headers = dict(request.headers)

            if not serializer:
                function = getattr(service, method_name)
                result = function(model, {}, {}, request.user, headers)
                return ResponseHandler.created(data=result.get("data"))

            serializer_instance = serializer(
                model=model,
                data=data,
                service=service,
                method_name=method_name,
                secret=secret,
                user=request.user,
            )
            if not serializer_instance.is_valid():
                raise ValidationError(serializer_instance.errors)

            function = getattr(service, method_name)
            result = function(
                model,
                serializer_instance.validated_data["value"],
                serializer_instance.validated_data.get("extra", {}),
                request.user,
                headers,
            )
            if method_name == "login" or result.get("type", "") == "raw":
                if result.get("type"):
                    result.pop("type")
                return ResponseHandler.raw(data=result)
            return ResponseHandler.created(data=result.get("data"))
        except ValidationError as ve:
            return ErrorHandler.error_response(
                f"Gagal menambahkan {data_name}", ve, 400
            )
        except Exception as e:
            return ErrorHandler.error_response(
                f"Gagal menambahkan {data_name}", str(e), 500
            )

    @staticmethod
    def update(method_name, request, pk, serializer, model, service, data_name):
        try:
            headers = dict(request.headers)
            result = BaseObjectUtil.get_object(
                model, data_name, pk, False, request.user
            )

            file_data = {
                field: (
                    request.FILES.getlist(field)[0]
                    if len(request.FILES.getlist(field)) == 1
                    else request.FILES.getlist(field)
                )
                for field in request.FILES
            }

            data = {**request.data, **file_data}
            form_data = request.data.get("form_data")
            if form_data:
                data.update(JsonUtil.smart_json_loads(form_data))

            BaseCRUDHandler.inject_company_id(data, request.user)

            secret = request.META.get("HTTP_X_SECRET")
            if not serializer:
                func = getattr(service, method_name)
                res = func(model, pk, result, {}, {}, request.user, headers)
                return ResponseHandler.updated(data=res.get("data"))

            serializer_instance = serializer(
                model=model,
                data=data,
                service=service,
                method_name=method_name,
                secret=secret,
                user=request.user,
            )
            if not serializer_instance.is_valid():
                raise ValidationError(serializer_instance.errors)

            func = getattr(service, method_name)
            res = func(
                model,
                pk,
                result,
                serializer_instance.validated_data["value"],
                serializer_instance.validated_data.get("extra", {}),
                request.user,
                headers,
            )
            return ResponseHandler.updated(data=res.get("data"))
        except ValidationError as ve:
            return ErrorHandler.error_response(f"Gagal update {data_name}", ve, 400)
        except Exception as e:
            return ErrorHandler.error_response(f"Gagal update {data_name}", str(e), 500)

    @staticmethod
    def destroy(method_name, request, pk, model, service, data_name):
        try:
            headers = dict(request.headers)
            result = BaseObjectUtil.get_object(
                model, data_name, pk, False, request.user
            )

            func = getattr(service, method_name)
            func(model, pk, result, request.user, headers)
            return ResponseHandler.deleted()
        except Exception as e:
            return ErrorHandler.error_response(
                f"Gagal menghapus {data_name}", str(e), 500
            )
