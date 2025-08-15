from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
import mimetypes


class ResponseUtil:
    @staticmethod
    def success(message, data=None, metadata=None, status_code=status.HTTP_200_OK):
        return Response(
            {
                "status": "success",
                "message": message,
                "data": data,
                "metadata": metadata,
            },
            status=status_code,
        )

    @staticmethod
    def error(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                "status": "error",
                "message": message,
                "errors": errors,
            },
            status=status_code,
        )

    @staticmethod
    def file(buffer, filename, content_type=None, as_attachment=True):
        extension_map = {
            "pdf": "application/pdf",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "xls": "application/vnd.ms-excel",
            "csv": "text/csv",
            "txt": "text/plain",
            "json": "application/json",
            "zip": "application/zip",
        }

        if content_type:
            content_type = content_type.lower()
            content_type = extension_map.get(content_type, content_type)
        else:
            content_type, _ = mimetypes.guess_type(filename)
            if content_type is None:
                content_type = "application/octet-stream"

        return FileResponse(
            buffer,
            as_attachment=as_attachment,
            filename=filename,
            content_type=content_type,
        )
