class RequestUtil:
    @staticmethod
    def parse_query_params(request):
        return {
            key: value[0] if isinstance(value, list) else value
            for key, value in request.query_params.lists()
        }

    @staticmethod
    def get_header_secret(request):
        return request.META.get("HTTP_X_SECRET", None)
