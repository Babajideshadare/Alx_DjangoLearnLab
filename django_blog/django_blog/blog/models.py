from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    """
    Diabetes Decoded blog post.
    Required fields per task:
    - title: CharField(200)
    - content: TextField
    - published_date: auto_now_add DateTime
    - author: FK to Django's User (one author -> many posts)
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    def __str__(self):
        return self.title