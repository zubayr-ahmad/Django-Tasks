# test_auth.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User

class AuthTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user("testuser", "test@test.com", "testpass")
    
    def test_token_auth(self):
        url = reverse("api_token_auth")
        data = {"username":"testuser", "password":"testpass"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token',response.data)
        self.token = response.data['token']
    
    def test_jwt_auth(self):
        url = reverse("jwt_token_obtain_pair")
        data = {"username":"testuser", "password":"testpass"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access',response.data)
    
    def test_signup(self):
        url = reverse("user_signup")
        data = {
            "username":"testuser2",
            "email":"testuser2@test.com",
            "password":"testpass2",
            "password_confirm":"testpass2"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.token = response.data['tokens']['access']
    