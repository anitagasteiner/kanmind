"""
Views for the authentication API of Kanmind.

This module defines API endpoints for user registration, login, and logout.
It uses token-based authentication with Django REST Framework's authtoken system.
"""

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer


class RegistrationView(APIView):
    """
    API view for registering a new user.

    Permissions:
        AllowAny: Anyone can register.
    
    Methods:
        post: Handle user registration, create user and token.
    """
        
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request to register a new user.

        Args:
            request: DRF Request object containing user data.

        Returns:
            Response with created user's token, fullname, email, and user_id if successful.
            Returns validation errors if input is invalid.
        """
                
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            fullname = f"{user.first_name} {user.last_name}".strip()
            return Response({
                'token': token.key,
                'fullname': fullname,
                'email': user.email,
                'user_id': user.id                
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    """
    API view for user login.

    Permissions:
        AllowAny: Anyone can attempt login.
    
    Methods:
        post: Authenticate user by email and password and return token.
    """
        
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request to log in a user.

        Args:
            request: DRF Request object containing 'email' and 'password'.

        Returns:
            Response with token, fullname, email, and user_id if authentication is successful.
            Returns error if credentials are missing or invalid.
        """
                
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if not user:
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        fullname = f"{user.first_name} {user.last_name}".strip()

        return Response({
            'token': token.key,
            'fullname': fullname,
            'email': user.email,
            'user_id': user.id
            }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    API view for user logout.

    Permissions:
        IsAuthenticated: Only logged-in users can log out.
    
    Methods:
        post: Deletes the current user's authentication token.
    """
        
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle POST request to log out a user.

        Args:
            request: DRF Request object containing the authenticated user.

        Returns:
            Response confirming logout and token deletion.
        """
                
        request.user.auth_token.delete()
        return Response({'detail': 'Logout successful. Token deleted.'}, status=status.HTTP_200_OK)

    