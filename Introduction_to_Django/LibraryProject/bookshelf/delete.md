from bookshelf.models import Book
b = Book.objects.get(title="Nineteen Eighty-Four")
b.delete()
# Output: (1, {'bookshelf.Book': 1})
list(Book.objects.all().values())
# Output: []