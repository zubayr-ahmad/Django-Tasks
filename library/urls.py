from django.urls import path
from .views import (BookListCreateView, 
                    BookRetrieveUpdateDestroyView,
                    AuthorListCreateView,
                    AuthorRetrieveUpdateDestroyView)
urlpatterns = [
    path('books/', BookListCreateView.as_view()),
    path('books/<int:pk>', BookRetrieveUpdateDestroyView.as_view()),
    path('authors/', AuthorListCreateView.as_view()),
    path('authors/<int:pk>', AuthorRetrieveUpdateDestroyView.as_view()),
]