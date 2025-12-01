"""
Root URL configuration for the Kanmind project.

This module defines the top-level URL routing:
- Admin interface
- Authentication API endpoints
- Kanban application API endpoints

Each included module provides its own URL patterns.
"""

from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),

    # Authentication endpoints
    path('api/', include('auth_app.api.urls')),

    # Kanban API endpoints
    path('api/', include('kanban_app.api.urls'))
]

