# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, timedelta

from accounts.permissions import MethodBasedPermission
from .models import Book, Author, Genre
from .serializers import BookSerializer, BookSerializerV2, AuthorSerializer, GenreSerializer
from .filters import BookFilter
from .utils import SerializerClassMixin
from .pagination import (CustomLimitOffsetPagination, 
                         CustomPageNumberPagination,
                         TimeBasePagination,
                         MetaDataPagination)

class AuthorViewSet(SerializerClassMixin, viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    serializer_class_mapping = {'v1':AuthorSerializer, 'v2':AuthorSerializer}
    queryset = Author.objects.all()
    # permission_classes = [ContentTypePermission]


class BookViewSet(SerializerClassMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('author').prefetch_related('genre')
    serializer_class_mapping = {'v1':BookSerializer, 'v2':BookSerializerV2}
    permission_classes = [MethodBasedPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'published_date', 'rating']
    filterset_class = BookFilter
    ordering_fields = ['title']
            
    def get_pagination_class(self):
        print(f"Request version: {self.request.version}")
        pagination_type = self.request.query_params.get('pagination', 'page')
        pagination_class = {
            'page': CustomPageNumberPagination,
            'cursor': TimeBasePagination,
            'meta': MetaDataPagination,
            'offset': CustomLimitOffsetPagination
        }
        return pagination_class[pagination_type]
    pagination_class = property(get_pagination_class)
    
    @action(detail=False,methods=['GET'])
    def recent(self, request, version=None):
        days = datetime.now().date() - timedelta(days=30)
        recent_books = Book.objects.filter(published_date__gt=days)
        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def stats(self, request, pk=None):
        book = self.get_object()
        return Response({
            "rating":book.rating,
            "days_ago": (datetime.now().date() - book.published_date).days
        })

    @action(detail=False, methods=['GET'])
    def featured(self, request, version=None):
        books = self.get_queryset().filter(is_featured=True)
        serialzer = self.get_serializer(books, many=True)
        return Response(serialzer.data)
    
    @action(detail=True, methods=['GET'], )
    def reviews(self, request, pk=None, version=None):
        if self.request.version != 'v2':
            return Response({"detail": "Reviews are only available in v2"}, status=status.HTTP_404_NOT_FOUND)
        book = self.get_object()
        # Mock reviews data for demonstration
        reviews = [{"id": 1, "content": f"Review of {book.title}", "rating": book.rating or 4.0}]
        return Response(reviews)
    # filterset_fields = ['title', 'is_featured']
    # filterset_class = BookFilter
    # search_fields = ['title', 'author__name']
    # ordering_fields = ['id']
    # pagination_class = MetaDataPagination

    # def get_queryset(self):
    #     queryset = Book.objects.all().select_related('author').prefetch_related('genre')
    #     return queryset

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return BookListSerializer
    #     if self.action == 'retrieve':
    #         return BookSerializer
    #     # if self.action in ('create', 'update', 'partial_update'):
    #     #     if self.request.user.is_staff:
    #     #         return BookAdminSerializer
    #     if 'fields' in self.request.query_params:
    #         return BookAdaptiveSerializer
    #     return BookSerializer
    
    

class GenreViewSet(SerializerClassMixin, viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    serializer_class_mapping = {'v1':GenreSerializer, 'v2': GenreSerializer}
    filter_backends = [SearchFilter]
    search_fields = ['label']

    queryset = Genre.objects.all()
