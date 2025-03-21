from django.urls import path
from .views import (BookListCreateView, 
                    BookRetrieveUpdateDestroyView,
                    AuthorListCreateView,
                    AuthorRetrieveUpdateDestroyView,
                    GenreListCreateView,
                    GenreRetrieveUpdateDestroyView
                    )
urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='books-list'),
    path('books/<int:pk>', BookRetrieveUpdateDestroyView.as_view(), name='books-detail'),
    path("authors/", AuthorListCreateView.as_view(), name="authors-list"),
    path("authors/<int:pk>/", AuthorRetrieveUpdateDestroyView.as_view(), name="authors-detail"),
    path('genres/', GenreListCreateView.as_view(), name='genres-list'),
    path('genres/<int:pk>', GenreRetrieveUpdateDestroyView.as_view(), name='genres-detail')
]