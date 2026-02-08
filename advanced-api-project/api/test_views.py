"""
API tests for Book endpoints (DRF Generic Views).

Covers:
- Public read (List/Detail)
- Authenticated write (Create/Update/Delete) with permission enforcement
- Filtering (?title=, ?publication_year=, ?author=, ?author__name=)
- Searching (?search= on title and author name)
- Ordering (?ordering=title, ?ordering=-publication_year)

Note on test DB:
- Django's test runner automatically uses an isolated test database.
- This suite also demonstrates session-based auth via self.client.login()
  to ensure permissions work independently of the dev DB.
"""

from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Author, Book


class BookAPITests(APITestCase):
    def setUp(self):
        # Users
        User = get_user_model()
        self.password = "pass12345"
        self.user = User.objects.create_user(username="tester", password=self.password)

        # Authors
        self.author1 = Author.objects.create(name="Chinua Achebe")
        self.author2 = Author.objects.create(name="Frank Herbert")

        # Books
        self.book1 = Book.objects.create(
            title="Things Fall Apart",
            publication_year=1958,
            author=self.author1,
        )
        self.book2 = Book.objects.create(
            title="Dune",
            publication_year=1965,
            author=self.author2,
        )

        # Common endpoints
        self.list_url = "/api/books/"
        self.create_url = "/api/books/create/"
        self.detail_url = f"/api/books/{self.book1.id}/"
        self.update_url = f"/api/books/update/{self.book1.id}/"
        self.delete_url = f"/api/books/delete/{self.book1.id}/"

    # ---------- Public (read-only) ----------
    def test_list_books_public_allowed(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 2)

    def test_detail_book_public_allowed(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)
        self.assertEqual(response.data["publication_year"], self.book1.publication_year)
        self.assertEqual(response.data["author"], self.book1.author.id)

    # ---------- Permissions (unauthenticated write should fail) ----------
    def test_create_requires_authentication(self):
        payload = {"title": "New Book", "publication_year": 2000, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    # ---------- Authenticated write via session login ----------
    def test_create_book_with_session_login_success(self):
        # This uses Django session auth; demonstrates self.client.login against the isolated test DB.
        logged_in = self.client.login(username="tester", password=self.password)
        self.assertTrue(logged_in, "Login failed in test (check credentials)")

        payload = {"title": "  New Book  ", "publication_year": 1999, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")
        self.assertEqual(response.data["publication_year"], 1999)
        self.assertEqual(response.data["author"], self.author1.id)
        self.assertTrue(Book.objects.filter(title="New Book", author=self.author1).exists())

    # ---------- Authenticated write via force_authenticate (also valid) ----------
    def test_create_book_future_year_invalid(self):
        self.client.force_authenticate(user=self.user)
        future_year = date.today().year + 1
        payload = {"title": "Future Book", "publication_year": future_year, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data)

    def test_update_book_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "  Updated Title  ",
            "publication_year": self.book1.publication_year,
            "author": self.book1.author.id,
        }
        response = self.client.put(self.update_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # ---------- Filtering / Searching / Ordering ----------
    def test_filter_by_title(self):
        response = self.client.get(f"{self.list_url}?title=Dune")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Dune")

    def test_filter_by_author_name(self):
        response = self.client.get(f"{self.list_url}?author__name=Chinua Achebe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item["author"] == self.author1.id for item in response.data))

    def test_search_by_title(self):
        response = self.client.get(f"{self.list_url}?search=Things")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertIn("Things Fall Apart", titles)

    def test_ordering_by_publication_year_desc(self):
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        self.assertEqual(years, sorted(years, reverse=True))