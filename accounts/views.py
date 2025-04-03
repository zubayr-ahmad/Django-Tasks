# views.py
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from rest_framework.status import HTTP_201_CREATED
from datetime import timedelta
from django.utils import timezone
from .serializers import TokenSerializer, CustomTokenObtainPairSerializer, UserSignupSerializer

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

class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'access_expires_at': timezone.now() + timedelta(days=1),
                'refresh_expires_at': timezone.now() + timedelta(days=2)
            }
        }, status=HTTP_201_CREATED)