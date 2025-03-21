import pytest
from rest_framework.test import APIClient
from datetime import date

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_author_data():
    return {
        "name": "John Smith",
        "bio": "An established writer from London",
        "date_of_birth": "1980-01-15"
    }

@pytest.fixture
def sample_genre_data():
    return {
        "label": "Mystery"
    }

@pytest.fixture
def sample_book_data(db, create_author):
    return {
        "title": "The Silent Echo",
        "author": create_author.id
    }

@pytest.fixture
def create_author(db):
    from library.models import Author
    author = Author.objects.create(
        name="Jane Doe",
        bio="A prolific fantasy author",
        date_of_birth=date(1975, 3, 20)
    )
    return author

@pytest.fixture
def create_genre(db):
    from library.models import Genre
    genre = Genre.objects.create(label="Fantasy")
    return genre

@pytest.fixture
def create_book(db, create_author):
    from library.models import Book
    book = Book.objects.create(
        title="Whispers in the Dark",
        author=create_author
    )
    return book