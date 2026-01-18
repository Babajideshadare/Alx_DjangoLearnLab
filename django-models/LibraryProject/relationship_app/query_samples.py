from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author.
books_by_author = Book.objects.filter(author__name="George Orwell")

# List all books in a library.
library = Library.objects.get(name="Central Library")
books_in_library = library.books.all()

# Retrieve the librarian for a library.
librarian_for_library = Librarian.objects.get(library=library)