# test_permissions.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from library.models import Book, Author, Genre
from accounts.models import User
from factories import UserFactory, BookFactory, AuthorFactory, GenreFactory
from utils import AuthAPIRequestFactory, create_user_with_role, validate_response_data
from library.views import BookViewSet
from django.conf import settings
class LibraryPermissionsTestCase(APITestCase):
    def setUp(self):
        self.user = create_user_with_role(username='testuser')
        self.staff_user = create_user_with_role(username="staffuser", role='staff')
        self.admin_user = create_user_with_role(username='adminuser', role='admin')
        self.author = Author.objects.create(name='testuser', bio='Bio', date_of_birth='2000-01-01')
        self.book = BookFactory(author=self.author)
        self.factory = AuthAPIRequestFactory
        self.version = settings.CURRENT_API_VERSION
    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_dummy(self):
        return True
    
    def test_unauthenticated_access(self):
        url = reverse('books-list', kwargs={'version': self.version})
        response = self.client.post(url, {'title': 'New Book', 'author': self.author.id}, format='json')
        validate_response_data(response, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_allowed_for_all_authenticated(self):
        url = reverse('books-list', kwargs={'version': self.version})
        self.authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_not_allowed_for_regular(self):
        url = reverse('books-list', kwargs={'version': self.version})
        data = {'title': 'Staff Book', 'author': self.author.id}
        self.authenticate(self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_post_allowed_for_regular(self):
        url = reverse('books-list', kwargs={'version': self.version})
        data = {'title': 'Updated Book', 'author': self.author.id, 'genre': 1}
        self.authenticate(self.staff_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_for_owner(self):
        """Owner is someone having same username and authorname"""
        url = reverse('books-detail', kwargs={'pk': self.book.id, 'version': self.version})
        data = {'title': 'Updated Book', 'author': self.author.id, 'genre': 1}
        factory = self.factory(self.user)
        request = factory.put(url, data=data)
        view = BookViewSet.as_view({'put':'update'})
        response = view(request, pk=self.book.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)