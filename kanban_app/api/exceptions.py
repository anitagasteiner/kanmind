from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import IntegrityError


def global_exception_handler(exc, context):
    # Erst DRFs Standard-Handler ausführen
    response = exception_handler(exc, context)

    # Falls DRF den Fehler bereits kennt → direkt zurückgeben
    if response is not None:
        return response

    # Eigene Fehlerbehandlungen
    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {"error": "Object not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if isinstance(exc, PermissionDenied):
        return Response(
            {"error": "Permission denied."},
            status=status.HTTP_403_FORBIDDEN
        )

    if isinstance(exc, IntegrityError):
        return Response(
            {"error": "Database integrity error."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Fallback für alle nicht zuvor abgefangenen Fehler
    return Response(
        {
            "error": "An unexpected error occurred.",
            "detail": str(exc),
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
