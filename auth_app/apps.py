"""
Django App configuration for the authentication app of Kanmind.

This module defines the configuration class for the `auth_app` Django application.
"""

from django.apps import AppConfig

class AuthAppConfig(AppConfig):
    """
    Configuration class for the authentication app.

    Attributes:
        default_auto_field (str): Default type for auto-generated primary keys.
        name (str): Name of the Django application.
    """
        
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'
