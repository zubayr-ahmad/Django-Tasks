from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        try:
            print("Middleware called")
            user_auth = self.jwt_authenticator.authenticate(request)
            if user_auth is not None:
                request.user, request.auth = user_auth
        except (InvalidToken, AuthenticationFailed):
            pass

        return self.get_response(request)