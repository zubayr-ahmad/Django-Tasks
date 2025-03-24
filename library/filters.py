from django_filters.rest_framework import FilterSet
from .models import Book
from rest_framework.filters import BaseFilterBackend

class BookFilter(FilterSet): 
    class Meta:
        model = Book
        fields = {
            'title': ['contains'],
            'published_date' : ['year__gte', 'year__lte'],            
            'is_featured': ['exact']
        }
        # fields = '__all__'

class BookAboveAvgFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        avg_rating = request.query_params.get("avg_rating")
        if avg_rating and avg_rating == 'true':
            return queryset.filter(rating__gte=4)
        return queryset