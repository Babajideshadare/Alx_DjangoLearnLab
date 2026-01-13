# Create
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
(book.id, book.title, book.author, book.publication_year)
# Output: (1, '1984', 'George Orwell', 1949)

# Retrieve
b = Book.objects.get(title="1984")
(b.id, b.title, b.author, b.publication_year)
# Output: (1, '1984', 'George Orwell', 1949)

# Update
b = Book.objects.get(title="1984")
b.title = "Nineteen Eighty-Four"
b.save()
(b.id, b.title, b.author, b.publication_year)
# Output: (1, 'Nineteen Eighty-Four', 'George Orwell', 1949)

# Delete
b = Book.objects.get(title="Nineteen Eighty-Four")
b.delete()
# Output: (1, {'bookshelf.Book': 1})
list(Book.objects.all().values())
# Output: []
