import mimetypes
from rest_framework.response import Response
from django.http import FileResponse


class ResponseHandler:
    @staticmethod
    def success(message=None, data=None, status_code=200, metadata=None):
        return Response(
            {
                "success": True,
                "message": message or "Berhasil",
                "data": data or [],
                "metadata": metadata or [],
            },
            status=status_code,
        )

    @staticmethod
    def created(message=None, data=None):
        return ResponseHandler.success(message or "Berhasil ditambahkan", data, 201)

    @staticmethod
    def updated(message=None, data=None):
        return ResponseHandler.success(message or "Berhasil diperbarui", data, 200)

    @staticmethod
    def deleted(message=None):
        return ResponseHandler.success(message or "Berhasil dihapus", None, 204)

    @staticmethod
    def raw(data, status_code=200):
        return Response(data, status=status_code)

    @staticmethod
    def file(buffer, filename, content_type=None, as_attachment=True):
        """
        Mengembalikan file sebagai response DRF dengan content type yang sesuai.
        """
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
