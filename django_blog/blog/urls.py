from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, register, profile

urlpatterns = [
    path("", home, name="home"),
    path("home/", home, name="home"),

    path("login/", LoginView.as_view(template_name="blog/auth/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="blog/auth/logged_out.html"), name="logout"),

    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
]