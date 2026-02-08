# Filtering, Searching, Ordering (DRF)

View: api/views.py → BookListView
- Filtering (DjangoFilterBackend): ?title=, ?publication_year=, ?author=, ?author__name=
- Searching (SearchFilter): ?search= on title and author name
- Ordering (OrderingFilter): ?ordering=title, ?ordering=-publication_year

Settings:
- INSTALLED_APPS includes 'django_filters' and 'rest_framework'.

Examples:
- /api/books/?author__name=Achebe
- /api/books/?search=Things
- /api/books/?ordering=-publication_year