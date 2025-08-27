class IgnoreTokenOnLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/user/login":
            request.COOKIES = request.COOKIES.copy()
            request.COOKIES.pop("access", None)
            request.COOKIES.pop("refresh", None)

            if "HTTP_AUTHORIZATION" in request.META:
                del request.META["HTTP_AUTHORIZATION"]

        response = self.get_response(request)
        return response
