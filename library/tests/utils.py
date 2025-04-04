from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User

class AuthAPIRequestFactory(APIRequestFactory):
    def __init__(self, user=None, token=None, **defaults):
        super().__init__(**defaults)
        self.user = user
        if token:
            self.token = token
        elif user:
            self.token = RefreshToken.for_user(user).access_token
        else:
            self.token = None
    
    def _add_auth_headers(self, kwargs):
        if self.token:
            kwargs.setdefault('HTTP_AUTHORIZATION', f'Bearer {self.token}')
        return kwargs

    def post(self, path, data=None, **extra):
        extra = self._add_auth_headers(extra)
        return super().post(path, data, **extra)
    
    def get(self, path, data=None, **extra):
        extra = self._add_auth_headers(extra)
        return super().get(path, data, **extra)
    
    def put(self, path, data=None, **extra):
        extra = self._add_auth_headers(extra)
        return super().put(path, data, **extra)
    
    def delete(self, path, data=None, **extra):
        extra = self._add_auth_headers(extra)
        return super().delete(path, data, **extra)
    