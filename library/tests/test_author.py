import pytest
from django.urls import reverse
from rest_framework import status
import json
from datetime import date

from library.models import Author
from library.serializers import AuthorSerializer


@pytest.mark.django_db
class TestAuthorAPI:
    def test_create_author(self, api_client, sample_author_data):
        url = reverse("authors-list")
        response = api_client.post(
            url, 
            data=json.dumps(sample_author_data),
            content_type="application/json"
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.count() == 1
        assert response.data["name"] == sample_author_data["name"]
        
    def test_get_author_list(self, api_client, create_author):
        url = reverse("authors-list")
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        
    def test_get_author_detail(self, api_client, create_author):
        url = reverse("authors-detail", kwargs={"pk": create_author.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == create_author.name
        assert "books" in response.data
        
    def test_update_author(self, api_client, create_author):
        url = reverse("authors-detail", kwargs={"pk": create_author.id})
        updated_data = {
            "name": "Jane Smith",
            "bio": "Updated biography with more details",
            "date_of_birth": "1975-03-20"
        }
        
        response = api_client.put(
            url,
            data=json.dumps(updated_data),
            content_type="application/json"
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == updated_data["name"]
        assert response.data["bio"] == updated_data["bio"]
        
    def test_delete_author(self, api_client, create_author):
        url = reverse("authors-detail", kwargs={"pk": create_author.id})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Author.objects.count() == 0
        
    def test_author_bio_validation(self, api_client):
        url = reverse("authors-list")
        invalid_data = {
            "name": "John Smith",
            "bio": "Hi",  # Too short, should fail validation
            "date_of_birth": "1980-01-15"
        }
        
        response = api_client.post(
            url,
            data=json.dumps(invalid_data),
            content_type="application/json"
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "bio" in response.data

@pytest.mark.django_db
class TestAuthorSerializer:
    def test_author_serialization(self, create_author):
        serializer = AuthorSerializer(create_author)
        
        assert serializer.data["name"] == create_author.name
        assert serializer.data["bio"] == create_author.bio
        assert serializer.data["date_of_birth"] == str(create_author.date_of_birth)
        assert "books" in serializer.data
        
    def test_author_deserialization(self, sample_author_data):
        serializer = AuthorSerializer(data=sample_author_data)
        
        assert serializer.is_valid()
        author = serializer.save()
        
        assert author.name == sample_author_data["name"]
        assert author.bio == sample_author_data["bio"]
        
    def test_author_bio_validation(self):
        invalid_data = {
            "name": "Test Author",
            "bio": "Hi",  # Too short
            "date_of_birth": "1990-01-01"
        }
        
        serializer = AuthorSerializer(data=invalid_data)
        
        assert not serializer.is_valid()
        assert "bio" in serializer.errors
        