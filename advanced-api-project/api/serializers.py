from datetime import date
from rest_framework import serializers
from .models import Author, Book

# BookSerializer serializes all fields of Book.
# Validation: publication_year must not be in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("publication_year cannot be in the future.")
        return value


# AuthorSerializer includes the author's name and a nested list of their books.
# Uses 'books' from Book.related_name, read-only nested representation.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ("name", "books")