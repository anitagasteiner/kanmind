"""
Custom authentication backend for Kanmind.

This backend allows users to authenticate using their email address instead of the username.
It is designed to work with Django's authentication system and Django REST Framework.
"""

from django.contrib.auth.models import User

class EmailAuthBackend:
    """
    Authentication backend that uses email and password for authentication.

    Methods:
        authenticate: Authenticate a user by email and password.
        get_user: Retrieve a User instance by ID.
    """
        
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user using their email and password.

        Args:
            request: The HTTP request object.
            username: Email address (passed by DRF as 'username').
            password: User password.
            **kwargs: Additional arguments (e.g., email).

        Returns:
            User instance if authentication is successful, None otherwise.
        """

        email = username or kwargs.get('email')
        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Retrieve a User instance by primary key (ID).

        Args:
            user_id: Primary key of the user.

        Returns:
            User instance if found, None otherwise.
        """
                
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
