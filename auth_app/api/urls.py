"""
URL configuration for the authentication API of Kanmind.

This module defines the endpoints for user registration, login, and logout.

Endpoints:
- /registration/ : Register a new user.
- /login/        : Authenticate a user and obtain a session or token.
- /logout/       : Logout the current user.
"""

from django.urls import path
from .views import RegistrationView, LoginView, LogoutView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
