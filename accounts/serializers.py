from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        attrs['user'] = user
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        return data

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 
            'first_name', 'last_name', 'is_staff', 'is_superuser',
            'is_active'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'is_active': {'default': True, 'required': False}
        }
    
    def validate(self, data):
        # Check that password entries match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords don't match"})
        
        # Only admin users can create staff or admin accounts
        request = self.context.get('request')
        if request and request.user and not request.user.is_anonymous:
            if (data.get('is_staff', False) or data.get('is_superuser', False)) and not request.user.is_superuser:
                raise serializers.ValidationError(
                    {"permission_denied": "You don't have permission to create staff or admin users"}
                )
        elif data.get('is_staff', False) or data.get('is_superuser', False):
            # If not authenticated (anonymous registration) but trying to create privileged user
            raise serializers.ValidationError(
                {"permission_denied": "You must be an admin to create staff or admin users"}
            )
            
        return data
    
    def create(self, validated_data):
        # Remove confirmation field from the data
        validated_data.pop('password_confirm')
        
        # Extract user role fields to handle them separately
        is_staff = validated_data.pop('is_staff', False)
        is_superuser = validated_data.pop('is_superuser', False)
        is_active = validated_data.pop('is_active', True)
        
        # Create base user first
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Set role attributes
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active
        
        # Save the user again with the role attributes
        user.save()
        
        return user