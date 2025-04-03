import pytest
from rest_framework.test import APIClient
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    return user

@pytest.fixture
def create_staff_user(db):
    user = User.objects.create_user(username='staffuser', password='staffpass', email='staff@example.com', is_staff=True)
    return user

@pytest.fixture
def create_admin_user(db):
    user = User.objects.create_superuser(username='adminuser', password='adminpass', email='admin@example.com')
    return user

