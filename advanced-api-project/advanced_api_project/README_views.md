# DRF Generic Views for Book

Endpoints (all under /api/):
- GET /books/ → List all books (public). Supports search via ?search= (title, author name).
- GET /books/<pk>/ → Retrieve a book (public).
- POST /books/create/ → Create a book (authenticated).
- PUT/PATCH /books/<pk>/update/ → Update a book (authenticated).
- DELETE /books/<pk>/delete/ → Delete a book (authenticated).

Permissions:
- List/Detail: AllowAny (public read).
- Create/Update/Delete: IsAuthenticated (must be logged in).

Customizations:
- perform_create/perform_update: trim title; validation handled by BookSerializer (publication_year cannot be in the future).
- BookListView uses SearchFilter for ?search= queries on title and author__name.

Files:
- api/views.py → DRF generic views
- api/urls.py → URL routes
- api/serializers.py → BookSerializer with validation, AuthorSerializer with nested books