from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view: list all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    lines = [f"{b.title} - {b.author.name}" for b in books]
    return HttpResponse("\n".join(lines) or "No books.", content_type="text/plain")

# Class-based view: details for a specific library
class LibraryDetailView(DetailView):
    model = Library

    def render_to_response(self, context, **response_kwargs):
        library = self.object
        books = library.books.select_related('author').all()
        lines = [f"Library: {library.name}"] + [f"{b.title} - {b.author.name}" for b in books]
        content = "\n".join(lines) if books else f"Library: {library.name}\nNo books."
        return HttpResponse(content, content_type="text/plain", **response_kwargs)