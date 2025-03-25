from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.name} : {self.bio}" 
    
class Genre(models.Model):
    label = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.label

class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='books'
    )
    genre = models.ManyToManyField(Genre, related_name='books')
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} : {self.author.name}"