import factory
from library.models import Book, Author, Genre
from accounts.models import User

# TODO: instead of random values, use simple ones for test cases. Also update test cases accordingly
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'testpass')

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    name = factory.Faker('name')
    bio = factory.Faker('text')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=20, maximum_age=80)

class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre
    
    label = factory.Faker('word')

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
    title = factory.Faker('sentence', nb_words=4)
    author = factory.SubFactory(AuthorFactory)
    rating = factory.Faker('pydecimal', left_digits=1, right_digits=1, min_value=1, max_value=5)
    is_featured = factory.Faker('boolean')

    @factory.post_generation
    def genre(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for genre in extracted:
                self.genre.add(genre)
        else:
            self.genre.add(GenreFactory())
