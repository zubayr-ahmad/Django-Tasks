from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class BookViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_date": "2023-01-01",
        }
