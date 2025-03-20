from rest_framework import serializers
from .models import Book, Author
import datetime
class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'date_of_birth', 'books']
        depth = 1
    
    def validate_bio(self, bio):
        if len(bio) <= 3:
            return serializers.ValidationError("Bio field should be more than 3 characters")


class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = AuthorSerializer()
    days_ago = serializers.SerializerMethodField(
        method_name='get_days_ago', read_only=True
    )    

    def get_days_ago(self, obj):
        # self serializer, obj = Book instance
        return obj.published_date

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'days_ago']
