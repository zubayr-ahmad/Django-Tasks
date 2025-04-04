from django.urls import reverse
from rest_framework import status
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
            self.token = get_jwt_token(user)
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

class CRUDTestMixin:
    model = None
    factory_class = None
    list_url_name = None
    detail_url_name = None

    def create_instance(self, **kwargs):
        return self.factory_class(**kwargs)

    def test_create(self):
        url = reverse(self.list_url_name)
        data = self.get_create_data()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.model.objects.count(), self.initial_count + 1)

    def test_retrieve_list(self):
        url = reverse(self.list_url_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_detail(self):
        instance = self.create_instance()
        url = reverse(self.detail_url_name, kwargs={'pk': instance.id})
        response = self.client.get(url)
        results = response.data.get('results', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(results['id'], instance.id)
        
    def test_update(self):
        instance = self.create_instance()
        url = reverse(self.detail_url_name, kwargs={'pk': instance.id})
        data = self.get_update_data(instance)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        count_before = self.model.objects.count()
        instance = self.create_instance()
        url = reverse(self.detail_url_name, kwargs={'pk': instance.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.model.objects.count(), count_before)

class AuthMixin:
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(self.user)

    def tearDown(self):
        self.client.force_authenticate(None)
        super().tearDown()

def get_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return refresh.access_token

def create_user_with_role(role='regular', **extras):
    username = extras.get('username', f'{role}')
    if role == 'staff':
        return User.objects.create_user(username=username, password='testpass', is_staff=True)
    elif role == 'admin':
        return User.objects.create_superuser(username=username, password='testpass')
    return User.objects.create_user(username=username, password='testpass')

def validate_response_data(response, expected_status=status.HTTP_200_OK,  expected_keys=None):
    assert response.status_code == expected_status
    if expected_keys:
        data = response.json()
        for key in expected_keys:
            assert key in data