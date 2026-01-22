from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.urls import path
from . import views

urlpatterns = [
    # Existing views
    path("books/", views.list_books, name="list_books"),
    path("libraries/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Auth
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),

    # Role-based views
    path("role/admin/", views.admin_view, name="admin_view"),
    path("role/librarian/", views.librarian_view, name="librarian_view"),
    path("role/member/", views.member_view, name="member_view"),
]

urlpatterns = [
    # existing URLs...
    path("books/add/", views.add_book, name="add_book"),
    path("books/<int:pk>/edit/", views.edit_book, name="edit_book"),
    path("books/<int:pk>/delete/", views.delete_book, name="delete_book"),
]