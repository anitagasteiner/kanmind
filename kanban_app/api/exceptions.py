"""
Custom global exception handler for the Kanmind API.

This module defines a unified exception-handling mechanism for all API views.
It extends Django REST Framework's default exception handler to ensure that
uncaught or framework-external errors are returned in a consistent and clean
JSON format.

Behavior:
- Known DRF exceptions are delegated to the standard DRF exception handler.
- Common Django exceptions such as ObjectDoesNotExist, PermissionDenied, and
  IntegrityError are converted into structured API responses.
- All other unhandled exceptions fall back to a generic 500 response containing an error message and minimal debug details.

Structure:
- global_exception_handler: Main entry point for DRF's EXCEPTION_HANDLER setting.

Handled cases:
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
