from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
    NotFound,
    MethodNotAllowed,
    Throttled,
)
from rest_framework.response import Response
from rest_framework import status
from utils.error_util import ErrorUtil

import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Extract context information
    view = context.get("view", "Unknown View")
    request = context.get("request", None)
    email = getattr(request.user, "email", "Anonymous") if request else "Anonymous"

    # Log the exception
    error_type = type(exc).__name__
    error_detail = str(exc)
    log_message = f"EXCEPTION: {error_type} | User: {email} | View: {view} | Detail: {error_detail}"
    logger.error(log_message)

    # Handle specific exceptions
    if isinstance(exc, AuthenticationFailed):
        logger.warning(f"AUTHENTICATION FAILED: {error_detail}")
        return Response(
            {"status": "error", "message": _("Autentikasi gagal.")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(exc, NotAuthenticated):
        return Response(
            {"status": "error", "message": _("Kredensial autentikasi tidak tersedia.")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(exc, PermissionDenied):
        return Response(
            {
                "status": "error",
                "message": _("Anda tidak memiliki izin untuk tindakan ini."),
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    if isinstance(exc, ValidationError):
        logger.warning(f"VALIDATION ERROR: {error_detail}")
        extracted_errors = ErrorUtil.extract_error(exc)
        return Response(
            {
                "status": "error",
                "message": _("Validasi gagal."),
                "errors": extracted_errors,
                "status_code": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, NotFound):
        return Response(
            {"status": "error", "message": _("Resource tidak ditemukan.")},
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, MethodNotAllowed):
        return Response(
            {"status": "error", "message": _("Metode HTTP tidak diizinkan.")},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    if isinstance(exc, Throttled):
        return Response(
            {"status": "error", "message": _("Permintaan melebihi batas rate limit.")},
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    # Fallback for unhandled exceptions
    response = exception_handler(exc, context)
    if response is not None:
        logger.error(f"DRF_EXCEPTION: {exc} | Status: {response.status_code}")
        custom_response_data = {
            "status": "error",
            "message": response.data.get("detail", _("Terjadi kesalahan.")),
            "errors": response.data if isinstance(response.data, dict) else None,
            "status_code": response.status_code,
        }
        return Response(custom_response_data, status=response.status_code)

    logger.critical(f"UNHANDLED ERROR: {error_detail}")
    custom_response_data = {
        "status": "error",
        "message": _("Terjadi kesalahan pada server. Silakan coba lagi nanti."),
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    if settings.DEBUG:
        custom_response_data["debug"] = {
            "type": error_type,
            "detail": error_detail,
        }

    return Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
