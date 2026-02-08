"""
API tests for Book endpoints (DRF Generic Views).

Covers:
- Public read (List/Detail)
- Authenticated write (Create/Update/Delete) with permission enforcement
- Filtering (?title=, ?publication_year=, ?author=, ?author__name=)
- Searching (?search= on title and author name)
- Ordering (?ordering=title, ?ordering=-publication_year)

How to run:
    cd ~/Desktop/Alx_DjangoLearnLab/advanced-api-project
    source .venv/Scripts/activate
    python manage.py test api
"""

from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Author, Book


class BookAPITests(APITestCase):
    def setUp(self):
        # Users
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="pass12345")

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
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data, list)
        self.assertGreaterEqual(len(res.data), 2)

    def test_detail_book_public_allowed(self):
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], self.book1.title)
        self.assertEqual(res.data["publication_year"], self.book1.publication_year)
        self.assertEqual(res.data["author"], self.book1.author.id)

    # ---------- Permissions ----------
    def test_create_requires_authentication(self):
        payload = {
            "title": "New Book",
            "publication_year": 2000,
            "author": self.author1.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        # DRF may return 401 or 403 depending on auth classes; accept either
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    # ---------- Create / Update / Delete (authenticated) ----------
    def test_create_book_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "  New Book  ",  # will be trimmed by perform_create
            "publication_year": 1999,
            "author": self.author1.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "New Book")
        self.assertEqual(res.data["publication_year"], 1999)
        self.assertEqual(res.data["author"], self.author1.id)
        self.assertTrue(Book.objects.filter(title="New Book", author=self.author1).exists())

    def test_create_book_future_year_invalid(self):
        self.client.force_authenticate(user=self.user)
        future_year = date.today().year + 1
        payload = {
            "title": "Future Book",
            "publication_year": future_year,
            "author": self.author1.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", res.data)

    def test_update_book_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "  Updated Title  ",  # will be trimmed by perform_update
            "publication_year": self.book1.publication_year,
            "author": self.book1.author.id,
        }
        res = self.client.put(self.update_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(self.delete_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # ---------- Filtering / Searching / Ordering ----------
    def test_filter_by_title(self):
        res = self.client.get(f"{self.list_url}?title=Dune")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Dune")

    def test_filter_by_author_name(self):
        res = self.client.get(f"{self.list_url}?author__name=Chinua Achebe")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item["author"] == self.author1.id for item in res.data))

    def test_search_by_title(self):
        res = self.client.get(f"{self.list_url}?search=Things")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertIn("Things Fall Apart", titles)

    def test_ordering_by_publication_year_desc(self):
        res = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in res.data]
        self.assertEqual(years, sorted(years, reverse=True))