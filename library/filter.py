from django_filters.rest_framework import FilterSet
from .models import Book

class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {
            'published_date' : ['gte', 'lte', 'exact'],            
            'is_featured': ['exact']
        }
        # fields = '__all__'