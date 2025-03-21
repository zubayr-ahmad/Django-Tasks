from django.urls import path
from .views import (BookListCreateView, 
                    BookRetrieveUpdateDestroyView,
                    AuthorListCreateView,
                    AuthorRetrieveUpdateDestroyView,
                    GenreListCreateView,
                    GenreRetrieveUpdateDestroyView
                    )
urlpatterns = [
    path('books/', BookListCreateView.as_view()),
    path('books/<int:pk>', BookRetrieveUpdateDestroyView.as_view(), name='books-detail'),
    path('authors/', AuthorListCreateView.as_view()),
    path('authors/<int:pk>', AuthorRetrieveUpdateDestroyView.as_view()),
    path('genres/', GenreListCreateView.as_view()),
    path('genres/<int:pk>', GenreRetrieveUpdateDestroyView.as_view())
]