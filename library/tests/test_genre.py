import pytest
from django.urls import reverse
from rest_framework import status
import json

from library.models import Genre
from library.serializers import GenreSerializer


@pytest.mark.django_db
class TestGenreAPI:
    
    def test_create_genre(self, api_client, sample_genre_data):
        url = reverse("genres-list")
        response = api_client.post(
            url,
            data=json.dumps(sample_genre_data),
            content_type="application/json"
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Genre.objects.count() == 1
        assert response.data["label"] == sample_genre_data["label"]
        
    def test_get_genre_list(self, api_client, create_genre):
        url = reverse("genres-list")
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        
    def test_get_genre_detail(self, api_client, create_genre):
        url = reverse("genres-detail", kwargs={"pk": create_genre.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["label"] == create_genre.label
        assert "books" in response.data
        
    def test_update_genre(self, api_client, create_genre):
        url = reverse("genres-detail", kwargs={"pk": create_genre.id})
        updated_data = {
            "label": "Science Fiction"
        }
        
        response = api_client.put(
            url,
            data=json.dumps(updated_data),
            content_type="application/json"
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["label"] == updated_data["label"]
        
    def test_delete_genre(self, api_client, create_genre):
        url = reverse("genres-detail", kwargs={"pk": create_genre.id})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Genre.objects.count() == 0
        
    def test_genre_unique_constraint(self, api_client, create_genre):
        url = reverse("genres-list")
        duplicate_data = {
            "label": "Fantasy"  # This should already exist from the fixture
        }
        
        response = api_client.post(
            url,
            data=json.dumps(duplicate_data),
            content_type="application/json"
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "label" in response.data

@pytest.mark.django_db
class TestGenreSerializer:
    
    def test_genre_serialization(self, create_genre):
        serializer = GenreSerializer(create_genre)
        
        assert serializer.data["label"] == create_genre.label
        assert "books" in serializer.data
        
    def test_genre_deserialization(self, sample_genre_data):
        serializer = GenreSerializer(data=sample_genre_data)
        
        assert serializer.is_valid()
        genre = serializer.save()
        
        assert genre.label == sample_genre_data["label"]