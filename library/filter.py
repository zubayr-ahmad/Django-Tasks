from django_filters.rest_framework import FilterSet
from .models import Book

class BookFilter(FilterSet):
    
    class Meta:
        model = Book
        fields = {
            'title': ['contains'],
            'published_date' : ['year__gte', 'year__lte'],            
            'is_featured': ['exact']
        }
        # fields = '__all__'