import logging
import re
from typing import List, Dict, Any, Union
from rest_framework.exceptions import ErrorDetail

logger = logging.getLogger(__name__)


class ErrorUtil:
    @staticmethod
    def extract_error(e: Exception) -> List[Dict[str, Union[str, Any]]]:
        if not isinstance(e, Exception):
            logger.error(f"Invalid input type for extract_error: {type(e)}")
            return [
                {
                    "field": "unknown",
                    "message": "Invalid input type",
                    "code": "invalid_input",
                }
            ]

        try:
            details = getattr(e, "detail", None)
        except AttributeError:
            details = None

        if not details:
            logger.warning(f"No 'detail' attribute found in exception: {e}")
            return [{"field": "unknown", "message": str(e), "code": "unknown_error"}]

        output = []
        try:
            if isinstance(details, dict):
                for field, errors in details.items():
                    if isinstance(errors, list) and len(errors) > 0:
                        for error in errors:
                            if isinstance(error, dict):
                                output.append(
                                    {
                                        "field": field,
                                        "message": error.get(
                                            "message", "Unknown error"
                                        ),
                                        "code": error.get("code", "unknown_code"),
                                    }
                                )
                            else:
                                output.append(
                                    {
                                        "field": field,
                                        "message": str(error),
                                        "code": "unknown_code",
                                    }
                                )
                    else:
                        output.append(
                            {
                                "field": field,
                                "message": str(errors),
                                "code": "unknown_code",
                            }
                        )
            elif isinstance(details, list):
                for error in details:
                    if isinstance(error, dict):
                        output.append(
                            {
                                "field": "non_field_errors",
                                "message": error.get("message", "Unknown error"),
                                "code": error.get("code", "unknown_code"),
                            }
                        )
                    else:
                        output.append(
                            {
                                "field": "non_field_errors",
                                "message": str(error),
                                "code": "unknown_code",
                            }
                        )
            else:
                output.append(
                    {
                        "field": "non_field_errors",
                        "message": str(details),
                        "code": "unknown_code",
                    }
                )
        except Exception as parse_error:
            logger.error(f"Failed to parse error details: {parse_error}")
            output.append(
                {"field": "unknown", "message": str(e), "code": "parsing_error"}
            )

        return output

    @staticmethod
    def standardize_error_response(error_message, field_errors=None):
        standardized_errors = {}

        if field_errors:
            standardized_errors.update(field_errors)

        if error_message:
            standardized_errors["non_field_error"] = [error_message]

        return standardized_errors

    @staticmethod
    def human_readable_message(error_details):
        duplicate_key_pattern = r"dup key: \{ (\w+): \"([^\"]+)\" \}"

        if isinstance(error_details, str):
            match = re.search(duplicate_key_pattern, error_details)
            if match:
                field_name = match.group(1)
                field_value = match.group(2)
                return f"{field_name.capitalize()} '{field_value}' sudah digunakan. Silakan gunakan nilai lain."
            if "[ErrorDetail(string=" in error_details:
                error_message = error_details.split("[ErrorDetail(string=")[1]
                error_message = error_message.split(",")[0].strip('"')
                return error_message
            else:
                return error_details

        return "Terjadi kesalahan. Silakan coba lagi."
