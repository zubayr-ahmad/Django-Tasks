# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, timedelta

from accounts.permissions import IsOwner, FieldLevelPermission, IPBasedPermission, MethodBasedPermission
from .models import Book, Author, Genre
from .serializers import BookSerializer, BookListSerializer, BookAdminSerializer, BookAdaptiveSerializer, AuthorSerializer, GenreSerializer
from .filters import BookFilter, BookAboveAvgFilterBackend
from .pagination import (CustomLimitOffsetPagination, 
                         CustomPageNumberPagination,
                         TimeBasePagination,
                         MetaDataPagination)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [IsOwner | (IPBasedPermission & FieldLevelPermission)]
    permission_classes = [MethodBasedPermission]
    filter_backends = [DjangoFilterBackend, 
                       SearchFilter, OrderingFilter, 
                    #    BookAboveAvgFilterBackend
                       ]

    def get_pagination_class(self):
        pagination_type = self.request.query_params.get('pagination', 'page')
        pagination_class = {
            'page': CustomPageNumberPagination,
            'cursor': TimeBasePagination,
            'meta': MetaDataPagination,
            'offset': CustomLimitOffsetPagination
        }
        return pagination_class[pagination_type]
    
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

    # filterset_fields = ['title', 'is_featured']
    # filterset_class = BookFilter
    # search_fields = ['title', 'author__name']
    # ordering_fields = ['id']
    # pagination_class = MetaDataPagination

    # def get_queryset(self):
    #     queryset = Book.objects.all().select_related('author').prefetch_related('genre')
    #     return queryset
    # pagination_class = property(get_pagination_class)

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
    
    

class GenreViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['label']

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
