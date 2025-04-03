from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from library.models import Book, Author, Genre
from accounts.models import User
from factories import UserFactory, BookFactory, AuthorFactory, GenreFactory

class LibraryPermissionsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.staff_user = UserFactory(username="staffuser", is_staff=True)
        self.admin_user = UserFactory(username='adminuser', is_staff=True, is_superuser=True)
        self.author = Author.objects.create(name='testuser', bio='Bio', date_of_birth='2000-01-01')
        self.book = BookFactory(author=self.author)
    
    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_dummy(self):
        return True
    
    def test_unauthenticated_access(self):
        url = reverse('books-list')
        response = self.client.post(url, {'title': 'New Book', 'author': self.author.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_allowed_for_all_authenticated(self):
        url = reverse('books-list')
        self.authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_not_allowed_for_regular(self):
        url = reverse('books-list')
        data = {'title': 'Staff Book', 'author': self.author.id}
        self.authenticate(self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_post_allowed_for_regular(self):
        url = reverse('books-list')
        data = {'title': 'Staff Book', 'author': self.author.id}
        self.authenticate(self.staff_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_for_owner(self):
        """Owner is someone having same username and authorname"""
        url = reverse('books-detail', kwargs={'pk': self.book.id})
        self.authenticate(self.user)
        response = self.client.put(url, {'title': 'Updated Book', 'author': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    