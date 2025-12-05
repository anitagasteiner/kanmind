"""
Custom global exception handler for the Kanmind API.

This module provides a unified exception-handling strategy for all API endpoints.
It extends Django REST Framework's built-in exception handler to ensure that
both framework-level and unexpected errors are returned in a consistent JSON
format.

Behavior:
- DRF-native exceptions are first delegated to DRF's default exception handler.
- Common Django exceptions (ObjectDoesNotExist, PermissionDenied, ValidationError, IntegrityError) are mapped to structured API responses with appropriate status codes.
- TypeError and ValueError are treated as client errors (400 Bad Request).
- Any remaining unhandled exceptions result in a generic 500 response that includes a minimal error description and the exception detail string.

Handled cases:
- Django/DRF ValidationError → 400 Bad Request
- TypeError, ValueError → 400 Bad Request
- ObjectDoesNotExist → 404 Not Found
- PermissionDenied → 403 Forbidden
- IntegrityError → 400 Bad Request
- All other exceptions → 500 Internal Server Error

This ensures consistent, predictable error formatting across the entire API.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import IntegrityError


def global_exception_handler(exc, context):
    """
    Global exception handler used by Django REST Framework.

    Args:
        exc: The raised exception.
        context: Additional context provided by DRF, including the view.

    Returns:
        A DRF Response object with a standardized error structure and the
        appropriate HTTP status code.
    """
    
    response = exception_handler(exc, context)

    if response is not None:
        return response
    
    if isinstance(exc, (DjangoValidationError, DRFValidationError)):
        return Response(
            {'error': exc.message},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if isinstance(exc, (TypeError, ValueError)):
        return Response(
            {'error': str(exc)},
            status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {'error': 'Object not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if isinstance(exc, PermissionDenied):
        return Response(
            {'error': 'Permission denied.'},
            status=status.HTTP_403_FORBIDDEN
        )

    if isinstance(exc, IntegrityError):
        return Response(
            {'error': 'Database integrity error.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {
            'error': 'An unexpected error occurred.',
            'detail': str(exc),
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
