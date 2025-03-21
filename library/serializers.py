from rest_framework import serializers
from .models import Book, Author, Genre
class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    books = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='books-detail' 
    )
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'date_of_birth', 'books']
        depth = 1
    
    def validate_bio(self, bio):
        if len(bio) <= 3:
            return serializers.ValidationError("Bio field should be more than 3 characters")
        return bio


class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all()
    )
    days_ago = serializers.SerializerMethodField(
        method_name='get_days_ago', read_only=True
    )    

    def get_days_ago(self, obj):
        # self serializer, obj = Book instance
        return obj.published_date

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'days_ago']
    
    def validate(self, obj):
        print(obj)
        if obj['author'] is None or obj['title'] is None:
            raise serializers.ValidationError("Author and title cannot be None")
        return obj

class GenreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ['id', 'label', 'books']
        # depth = 1