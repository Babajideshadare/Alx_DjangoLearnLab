# Authentication (Django Blog)

Features:
- Register (/register) using a custom RegistrationForm (extends UserCreationForm with email).
- Login (/login) and logout (/logout) via Django’s built-in auth views.
- Profile (/profile) to view and edit first/last name and email (login required).

Templates:
- blog/templates/blog/auth/login.html
- blog/templates/blog/auth/register.html
- blog/templates/blog/auth/profile.html
- blog/templates/blog/auth/logged_out.html

Settings:
- LOGIN_URL = "login"
- LOGIN_REDIRECT_URL = "home"
- LOGOUT_REDIRECT_URL = "home"

Testing:
- Register a user at /register, then login at /login.
- Update profile at /profile.
- Logout at /logout.