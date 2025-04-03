import pytest
from rest_framework import status
from django.urls import reverse
import json

@pytest.mark.django_db
class TestAuthentication:
    def test_token_auth_success(self, api_client, create_user):
        url = reverse('api_token_auth')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert response.data['username'] == 'testuser'

    def test_token_auth_failure(self, api_client):
        url = reverse('api_token_auth')
        data = {'username': 'wronguser', 'password': 'wrongpass'}
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data

    def test_jwt_auth_success(self, api_client, create_user):
        url = reverse('jwt_token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['username'] == 'testuser'

    def test_jwt_auth_failure(self, api_client):
        url = reverse('jwt_token_obtain_pair')
        data = {'username': 'wronguser', 'password': 'wrongpass'}
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data

    def test_jwt_refresh(self, api_client, create_user):
        # First get tokens
        url = reverse('jwt_token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = api_client.post(url, data=json.dumps(data), content_type='application/json')
        refresh_token = response.data['refresh']
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        
        # Refresh token
        refresh_url = reverse('jwt_token_refresh')
        response = api_client.post(refresh_url, data=json.dumps({'refresh': refresh_token}), content_type='application/json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data