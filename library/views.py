from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author, Genre
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer
from .filter import BookFilter
from datetime import datetime, timedelta
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'is_featured']
    filterset_class = BookFilter

    @action(detail=False,methods=['GET'])
    def recent(self, request):
        days = datetime.now().date() - timedelta(days=30)
        recent_books = Book.objects.filter(published_date__gt=days)
        serializer = BookSerializer(recent_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def stats(self, request, pk=None):
        book = self.get_object()
        return Response({
            "rating":book.rating,
            "days_ago": (datetime.now().date() - book.published_date).days
        })

    @action(detail=False, methods=['GET'])
    def featured(self, request):
        books = self.get_queryset().filter(is_featured=True)
        serialzer = self.get_serializer(books, many=True)
        return Response(serialzer.data)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
