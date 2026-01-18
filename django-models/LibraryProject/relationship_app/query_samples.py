from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author.
author_name = "George Orwell"
books_by_author = Book.objects.filter(author__name=author_name)

# List all books in a library.
library_name = "Central Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()

# Retrieve the librarian for a library.
librarian_for_library = Librarian.objects.get(library=library)