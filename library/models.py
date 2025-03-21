from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.name} : {self.bio}" 
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, 
                               related_name='books')

    def __str__(self):
        return f"{self.title} : {self.author.name}"


    
    
