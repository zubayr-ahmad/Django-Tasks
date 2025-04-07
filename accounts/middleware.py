from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.deprecation import MiddlewareMixin
import re

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



class DeprecationMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        version_match = re.search(r'/(v\d)/', request.path)
        version = version_match.group(1) if version_match else None
        
        print(f"URL: {request.path}, Direct version: {version}, DRF version: {getattr(request, 'version', 'NOT SET')}")
        
        if version == 'v1':
            response['X-API-Deprecation-Warning'] = 'API v1 is deprecated and will be removed in future releases. Please upgrade to v2.'
        return response