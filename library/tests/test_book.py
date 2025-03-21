import pytest
from django.urls import reverse
from rest_framework import status
import json

from library.models import Book
from library.serializers import BookSerializer


@pytest.mark.django_db
class TestBookAPI:
    
    def test_create_book(self, api_client, sample_book_data):
        url = reverse("books-list")
        response = api_client.post(
            url,
            data=json.dumps(sample_book_data),
            content_type="application/json"
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.count() == 1
        assert response.data["title"] == sample_book_data["title"]
        
    def test_get_book_list(self, api_client, create_book):
        url = reverse("books-list")
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        
    def test_get_book_detail(self, api_client, create_book):
        url = reverse("books-detail", kwargs={"pk": create_book.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == create_book.title
        assert "days_ago" in response.data
        
    def test_update_book(self, api_client, create_book, create_author):
        url = reverse("books-detail", kwargs={"pk": create_book.id})
        updated_data = {
            "title": "Updated Book Title",
            "author": create_author.id
        }
        
        response = api_client.put(
            url,
            data=json.dumps(updated_data),
            content_type="application/json"
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == updated_data["title"]
        
    def test_delete_book(self, api_client, create_book):
        url = reverse("books-detail", kwargs={"pk": create_book.id})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Book.objects.count() == 0
        
    def test_book_validation(self, api_client, create_author):
        url = reverse("books-list")
        invalid_data = {
            "title": None,
            "author": create_author.id
        }
        
        response = api_client.post(
            url,
            data=json.dumps(invalid_data),
            content_type="application/json"
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_book_serialization(self, api_client, create_book):
        url = reverse("books-detail", kwargs={"pk": create_book.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        book_serializer = BookSerializer(create_book)
        assert response.data["title"] == book_serializer.data["title"]
        assert "published_date" in response.data
        assert "days_ago" in response.data

@pytest.mark.django_db
class TestBookSerializer:
    
    def test_book_serialization(self, create_book):
        serializer = BookSerializer(create_book)
        
        assert serializer.data["title"] == create_book.title
        assert serializer.data["author"] == create_book.author.id
        assert "days_ago" in serializer.data
        
    def test_book_deserialization(self, sample_book_data):
        serializer = BookSerializer(data=sample_book_data)
        
        assert serializer.is_valid()
        book = serializer.save()
        
        assert book.title == sample_book_data["title"]
        assert book.author.id == sample_book_data["author"]
        
    def test_book_validation(self, create_author):
        invalid_data = {
            "title": None,
            "author": None
        }
        
        serializer = BookSerializer(data=invalid_data)
        
        assert not serializer.is_valid()