from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import CustomAuthToken, RefreshTokenView, CustomTokenObtainPairView


urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('refresh/', RefreshTokenView.as_view(), name='api_token_refresh'),
    path('jwt/login/', CustomTokenObtainPairView.as_view(), name='jwt_token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_token_verify'),

]