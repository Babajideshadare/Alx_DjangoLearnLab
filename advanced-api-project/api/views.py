from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer

# ListView: GET /api/books/ (public)
# - Adds simple search by title and author name using DRF's SearchFilter.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "author__name"]


# DetailView: GET /api/books/<pk>/ (public)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# CreateView: POST /api/books/create/ (authenticated)
# - Customizes behavior by trimming title and relying on serializer validation
#   (publication_year must not be in the future).
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title", "").strip()
        serializer.save(title=title)


# UpdateView: PUT/PATCH /api/books/<pk>/update/ (authenticated)
# - Customizes behavior by trimming title and letting serializer validate input.
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        title = serializer.validated_data.get("title", "").strip()
        serializer.save(title=title)


# DeleteView: DELETE /api/books/<pk>/delete/ (authenticated)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]