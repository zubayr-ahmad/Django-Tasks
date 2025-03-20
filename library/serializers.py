from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date']

