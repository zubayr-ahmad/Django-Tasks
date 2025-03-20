from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView
urlpatterns = [
    path('books/', BookListCreateView.as_view()),
    path('books/<int:pk>', BookRetrieveUpdateDestroyView.as_view())
]