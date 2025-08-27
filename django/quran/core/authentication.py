from rest_framework_simplejwt.authentication import JWTAuthentication
from constants.token import TOKEN_NAME


class FlexibleJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        raw_token = None

        if header is not None:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            raw_token = request.COOKIES.get(TOKEN_NAME.ACCESS_TOKEN)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
