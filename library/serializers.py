# serializers.py
from rest_framework import serializers
from accounts.permissions import FieldLevelPermission
from .models import Book, Author, Genre
from datetime import datetime
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
            raise serializers.ValidationError("Bio field should be more than 3 characters")
        return bio

class BookSerializer(serializers.ModelSerializer):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     view = self.context.get('view')
    #     if view and any(isinstance(p, FieldLevelPermission) for p in view.permission_classes):
    #         FieldLevelPermission(request=self.context['request']).filter_serializer_fields(self)
            
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all()
    )
    days_ago = serializers.SerializerMethodField(
        method_name='get_days_ago', read_only=True
    )    
    def get_days_ago(self, obj):
        # self serializer, obj = Book instance
        if obj.published_date:
            days_ago = (datetime.now().date() - obj.published_date).days
            return days_ago
        return None

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'days_ago', 'rating', 'is_featured', 'genre']
    
    def validate(self, obj):
        print(obj)
        if obj['author'] is None or obj['title'] is None:
            raise serializers.ValidationError("Author and title cannot be None")
        return obj

class BookSerializerV2(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all()
    )
    days_ago = serializers.SerializerMethodField(
        method_name='get_days_ago', read_only=True
    )   
    is_new = serializers.SerializerMethodField() 
    summary = serializers.CharField(allow_blank=True, required=False)
    def get_days_ago(self, obj):
        # self serializer, obj = Book instance
        if obj.published_date:
            days_ago = (datetime.now().date() - obj.published_date).days
            return days_ago
        return None
    
    def get_is_new(self, obj):
        if obj.published_date:
            is_new = (datetime.now().date() - obj.published_date).days <= 30
            return is_new
        return None

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'days_ago', 'rating', 'is_featured', 'genre', 'is_new', 'summary']
    
    def validate(self, obj):
        print(obj)
        if obj['author'] is None or obj['title'] is None:
            raise serializers.ValidationError("Author and title cannot be None")
        return obj


class BookListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only = True)
    genres = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='genres-list')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author_name', 'is_featured', 'genres']

class BookAdminSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all()
    )
    special_request = serializers.SerializerMethodField()

    def get_special_request(self, obj):
        return "authenticated"
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'rating', 'is_featured', 'special_request']

class BookAdaptiveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all()
    )
    days_ago = serializers.SerializerMethodField(
        method_name='get_days_ago', read_only=True
    )    

    def get_days_ago(self, obj):
        # self serializer, obj = Book instance
        if obj.published_date:
            days_ago = (datetime.now().date() - obj.published_date).days
            return days_ago
        return None

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'days_ago', 'rating', 'is_featured']
        all_fields = fields + ['genres']
    
    def validate(self, obj):
        print(obj)
        if obj['author'] is None or obj['title'] is None:
            raise serializers.ValidationError("Author and title cannot be None")
        return obj
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        requested_fields = request.query_params.get('fields').split(',')
        if request and requested_fields:
            allowed = set(self.Meta.all_fields)
            existing = set(self.fields)
            fields_to_remove = existing - (set(requested_fields) & allowed)
            for field_name in fields_to_remove:
                self.fields.pop(field_name)
            


class GenreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ['id', 'label', 'books']
        # depth = 1