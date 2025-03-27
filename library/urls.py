# urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (AuthorViewSet,
                    BookViewSet,
                    GenreViewSet
                    )

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'books', BookViewSet, basename='books')
router.register(r'genres', GenreViewSet, basename='genres')

urlpatterns = router.urls


# urlpatterns = [
#     path('books/', BookListCreateView.as_view(), name='books-list'),
#     path('books/<int:pk>', BookRetrieveUpdateDestroyView.as_view(), name='books-detail'),
#     path("authors/", AuthorListCreateView.as_view(), name="authors-list"),
#     path("authors/<int:pk>/", AuthorRetrieveUpdateDestroyView.as_view(), name="authors-detail"),
#     path('genres/', GenreListCreateView.as_view(), name='genres-list'),
#     path('genres/<int:pk>', GenreRetrieveUpdateDestroyView.as_view(), name='genres-detail')
# ]