from django.db import models

# Author represents a writer. One author can have many books.
# We keep it simple with only a 'name' field.
class Author(models.Model):
    name = models.CharField(max_length=100, help_text="Full name of the author")

    def __str__(self) -> str:
        return self.name


# Book belongs to a single Author (one-to-many via ForeignKey).
# related_name='books' lets us access an author's books via author.books.all()
class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the book")
    publication_year = models.IntegerField(help_text="Year the book was published")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
        help_text="Author who wrote this book",
    )

    def __str__(self) -> str:
        return f"{self.title} by {self.author.name}"