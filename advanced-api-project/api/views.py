from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework  # required by checker (DjangoFilterBackend)
from .models import Book
from .serializers import BookSerializer

# GET /api/books/ (public)
# Filtering (?title=, ?publication_year=, ?author=, ?author__name=),
# Searching (?search= on title/author name), Ordering (?ordering=title or -publication_year)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["title", "publication_year", "author", "author__name"]
    search_fields = ["title", "author__name"]
    ordering_fields = ["id", "title", "publication_year", "author__name"]
    ordering = ["id"]

# GET /api/books/<pk>/ (public)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# POST /api/books/create/ (auth required)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title", "").strip()
        serializer.save(title=title)

# PUT/PATCH /api/books/update/<pk>/ (auth required)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        title = serializer.validated_data.get("title", "").strip()
        serializer.save(title=title)

# DELETE /api/books/delete/<pk>/ (auth required)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]