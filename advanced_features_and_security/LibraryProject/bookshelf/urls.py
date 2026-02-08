from django.urls import path
from .views import book_list, book_create, book_edit, book_delete, form_example

app_name = "bookshelf"

urlpatterns = [
    path("", book_list, name="book_list"),
    path("create/", book_create, name="book_create"),
    path("<int:pk>/edit/", book_edit, name="book_edit"),
    path("<int:pk>/delete/", book_delete, name="book_delete"),
    path("form/", form_example, name="form_example"),
]