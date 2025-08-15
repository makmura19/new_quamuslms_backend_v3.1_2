from rest_framework.response import Response


class ResponseHelper:
    @staticmethod
    def success(http_action=None, message=None, data=None, metadata=None):
        default_messages = {
            "GET": "Data berhasil ditemukan",
            "POST": "Input data berhasil",
            "PUT": "Update data berhasil",
            "DELETE": "Hapus data berhasil",
            "DEFAULT": "Operasi berhasil dilakukan",
        }

        final_message = (
            message
            if message
            else default_messages.get(http_action, default_messages["DEFAULT"])
        )

        response = {
            "status": "success",
            "message": final_message,
            "data": data if data is not None else [],
            "metadata": metadata if metadata else {},
        }
        return Response(response)

    @staticmethod
    def error(message=None, errors=None, status_code=400):
        default_error_message = "Terjadi kesalahan saat memproses permintaan"

        response = {
            "status": "error",
            "message": message if message else default_error_message,
            "errors": errors if errors else [],
        }
        return Response(response, status=status_code)
