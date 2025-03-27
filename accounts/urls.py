from django.urls import path
from .views import CustomAuthToken, RefreshTokenView

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('refresh/', RefreshTokenView.as_view(), name='api_token_refresh'),
]