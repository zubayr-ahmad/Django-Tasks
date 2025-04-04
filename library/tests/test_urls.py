# test_urls.py
from django.test import TestCase
from django.urls import reverse, resolve
from library.views import BookViewSet, AuthorViewSet, GenreViewSet

class URLPatternsTestCase(TestCase):
    version = 'v1'
    def test_books_list_url(self):
        url = reverse('books-list', kwargs={'version': self.version})
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, BookViewSet)
        self.assertEqual(resolver.view_name, 'books-list')

    def test_books_detail_url(self):
        url = reverse('books-detail', kwargs={'pk': 1, 'version': self.version})
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, BookViewSet)
        self.assertEqual(resolver.view_name, 'books-detail')

    def test_authors_list_url(self):
        url = reverse('authors-list', kwargs={'version': self.version})
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, AuthorViewSet)
        self.assertEqual(resolver.view_name, 'authors-list')

    def test_genres_list_url(self):
        url = reverse('genres-list', kwargs={'version': self.version})
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, GenreViewSet)
        self.assertEqual(resolver.view_name, 'genres-list')