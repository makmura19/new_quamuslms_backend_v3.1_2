from rest_framework.response import Response
from rest_framework.exceptions import (
    APIException,
    ValidationError,
    AuthenticationFailed,
)
from constants.duplicate_error_map import DUPLICATE_ERROR_MAP


class ErrorHandler:
    @staticmethod
    def format_errors(error):
        def _stringify_error(e):
            if isinstance(e, str):
                return e
            try:
                return str(e)
            except Exception:
                return ""

        error_str = _stringify_error(error)
        if "duplicate key" in error_str:
            for field, label in DUPLICATE_ERROR_MAP.items():
                if field in error_str:
                    return {
                        "non_field_errors": [
                            f"Input Data Gagal, {label} sudah terdaftar."
                        ]
                    }
            return {
                "non_field_errors": [
                    "Input Data Gagal karena data sudah terdaftar (duplicate)."
                ]
            }

        if isinstance(error, ValidationError):
            detail = error.detail
            if isinstance(detail, list):
                return {"non_field_errors": detail}
            elif isinstance(detail, dict):
                return detail
            else:
                return {"non_field_errors": [_stringify_error(detail)]}

        elif isinstance(error, dict):
            return error

        elif isinstance(error, list):
            return {"non_field_errors": error}

        elif isinstance(error, str):
            return {"non_field_errors": [error]}

        else:
            return {"non_field_errors": [_stringify_error(error)]}

    @staticmethod
    def validation_error(detail, status_code=400):
        raise ValidationError(detail)

    @staticmethod
    def auth_error(detail="Authentication Failed"):
        raise AuthenticationFailed(detail)

    @staticmethod
    def api_exception(message, status_code=500):
        raise APIException(detail=message)

    @staticmethod
    def error_response(message, error_detail=None, status_code=400):
        print("❌ Error Detail:", error_detail)
        return Response(
            {
                "success": False,
                "message": message or "Terjadi kesalahan",
                "errors": ErrorHandler.format_errors(error_detail),
            },
            status=status_code,
        )

    @staticmethod
    def not_found(message="Data tidak ditemukan"):
        return ErrorHandler.error_response(message, status_code=404)

    @staticmethod
    def unauthorized(message="Tidak diizinkan"):
        return ErrorHandler.error_response(message, status_code=403)
