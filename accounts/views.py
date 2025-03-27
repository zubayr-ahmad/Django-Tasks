from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenSerializer, CustomTokenObtainPairSerializer
from datetime import timedelta
from django.utils import timezone
class CustomAuthToken(ObtainAuthToken):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        expires_at = timezone.now() + timedelta(hours=24)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'expires_at': expires_at
        })

class RefreshTokenView(ObtainAuthToken):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        token = Token.objects.create(user=request.user)
        expires_at = timezone.now() + timedelta(hours=24)
        
        return Response({
            'token': token.key,
            'expires_at': expires_at.isoformat()
        })
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer