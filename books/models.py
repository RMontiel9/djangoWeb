from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
    google_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, blank=True)
    thumbnail = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # Evita duplicados

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    CHOICES = [
        (1, '1 estrella'),
        (2, '2 estrellas'),
        (3, '3 estrellas'),
        (4, '4 estrellas'),
        (5, '5 estrellas'),
    ]
    rating = models.IntegerField(choices=CHOICES, default=5)
    comment = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rating}"