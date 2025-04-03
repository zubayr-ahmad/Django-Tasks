from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from library.models import Book, Author, Genre
from accounts.models import User
from factories import UserFactory, BookFactory, AuthorFactory, GenreFactory
class LibraryAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.book = BookFactory()
        self.author = self.book.author
        self.genre = self.book.genre.first()
    
    def test_get_books(self):
        url = reverse('books-list')
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        # self.assertEqual(response.data['results'][0]['title'], 'Test Book')

    def test_get_book_detail(self):
        url = reverse('books-detail', kwargs={'pk': self.book.id})
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['author'], self.author.pk)
    
    def test_create_book(self):
        url = reverse('books-list')
        data = {'title':'Test01', 'author':self.author.id, 'rating':4.0}
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_authors_list(self):
        url = reverse('authors-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # self.assertEqual(response.data['results'][0]['name'], 'Test Author')
    
    def test_create_author(self):
        url = reverse('authors-list')
        data = {'name': 'Author 2', 'bio': 'Bio 2', 'date_of_birth': '2003-01-01'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_get_genres_list(self):
        url = reverse('genres-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_genre(self):
        url = reverse('genres-list')
        data = {'label': 'Action'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)

class LibraryFilteringTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.author = AuthorFactory()
        self.genre = GenreFactory()
        self.book1 = BookFactory(title="Book A", author=self.author, genre=[self.genre], is_featured=True)
        self.book2 = BookFactory(title="Book B", author=self.author, genre=[self.genre], is_featured=False)
    
    def test_filter_by_title(self):
        url = reverse('books-list') + '?title__contains=A'
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Book A')
    
    def test_sorting_by_title(self):
        url = reverse('books-list') + '?ordering=title'
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Book A')
    
    def test_page_pagination(self):
        url = reverse('books-list') + '?pagination=page&page_size=1&page=1'
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
