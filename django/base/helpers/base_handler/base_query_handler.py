from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.response import Response
from utils.dict_util import DictUtil
from utils.request_util import RequestUtil
from utils.response_handler import ResponseHandler
from utils.error_handler import ErrorHandler
from constants.params_validation_type import ParamsValidationType
from constants.access import SCHOOL_ROLES, HOLDING_ROLES
import os


class BaseQueryHandler:
    @staticmethod
    def add_ownership(user, query_params, params_validation, model):
        company_id = os.environ.get("COMPANY_ID") or "school_id"
        schema_fields = [k for k, v in model.schema._declared_fields.items()]
        if (
            user
            and any(role in user.role.split(",") for role in SCHOOL_ROLES)
            and "school_id" in schema_fields
        ):
            query_params = {**query_params, "school_id": user.school_id}
            params_validation = {
                **params_validation,
                "school_id": ParamsValidationType.OBJECT_ID,
            }

        if (
            user
            and any(role in user.role.split(",") for role in HOLDING_ROLES)
            and "holding_id" in schema_fields
        ):
            query_params = {**query_params, "holding_id": user.holding_id}
            params_validation = {
                **params_validation,
                "holding_id": ParamsValidationType.OBJECT_ID,
            }
        return query_params, params_validation

    @staticmethod
    def extract_validation_params(params_validation: dict):
        data = {}
        required = []
        for key, value in params_validation.items():
            if key.endswith("__req"):
                clean_key = key.replace("__req", "")
                required.append(clean_key)
            else:
                clean_key = key
            data[clean_key] = value
        return data, required

    @staticmethod
    def list(
        method_name,
        request,
        model,
        service,
        data_name,
        params_validation,
    ):
        try:
            headers = dict(request.headers)
            tz = headers.get("X-Timezone", "UTC")
            if model:
                model.set_timezone(tz)

            params_validation, required_fields = (
                BaseQueryHandler.extract_validation_params(params_validation)
            )
            query_params = RequestUtil.parse_query_params(request)

            if not all(field in query_params for field in required_fields):
                raise ValidationError("Required Params is missing.")

            function_to_call = getattr(service, method_name, None)
            if not function_to_call:
                raise NotImplementedError(
                    f"Method {method_name} tidak ditemukan di service."
                )
            query_params, params_validation = BaseQueryHandler.add_ownership(
                request.user, query_params, params_validation, model
            )

            result = function_to_call(
                model, query_params, params_validation, request.user, headers
            )

            if not isinstance(result, dict):
                return result
            if "buffer" in result:
                type_ = result.get("type")
                return ResponseHandler.file(
                    result["buffer"], "downloaded_file", type_, True
                )
            return ResponseHandler.success(
                f"Data {data_name} berhasil ditemukan",
                data=result.get("data"),
                metadata=result.get("metadata"),
            )

        except (ValidationError, AuthenticationFailed) as e:
            return ErrorHandler.error_response(
                f"Gagal mengambil daftar {data_name}", str(e), status_code=400
            )
        except Exception as e:
            return ErrorHandler.error_response(
                f"Internal error mengambil daftar {data_name}", str(e), status_code=500
            )

    @staticmethod
    def retrieve(
        method_name,
        request,
        pk,
        model,
        service,
        data_name,
        is_owned=False,
    ):
        try:
            headers = dict(request.headers)
            function_to_call = getattr(service, method_name, None)
            if not function_to_call:
                raise NotImplementedError(
                    f"Method {method_name} tidak ditemukan di service."
                )

            query_params = RequestUtil.parse_query_params(request)
            params_validation = {}

            if is_owned:
                query_params, params_validation = DictUtil.add_ownership(
                    request.user, query_params, params_validation
                )

            result = function_to_call(
                model=model,
                _id=pk,
                user=request.user,
                headers_dict=headers,
                query_params=query_params,
                params_validation=params_validation,
            )

            if not result:
                raise ValidationError(f"{data_name} tidak ditemukan")

            if "buffer" in result:
                type_ = result.get("type")
                return ResponseHandler.file(
                    result["buffer"], "downloaded_file", type_, True
                )

            return ResponseHandler.success(
                f"Data {data_name} berhasil ditemukan", data=result
            )

        except (ValidationError, AuthenticationFailed) as e:
            return ErrorHandler.error_response(
                f"Gagal mengambil {data_name}", str(e), status_code=400
            )
        except Exception as e:
            return ErrorHandler.error_response(
                f"Internal error mengambil {data_name}", str(e), status_code=500
            )
