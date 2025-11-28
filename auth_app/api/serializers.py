"""
Serializers for the authentication API of Kanmind.

This module defines the serializer for user registration and validation.
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Fields:
        password (str): User password (write-only).
        repeated_password (str): Confirmation of the password (write-only).
        fullname (str): Full name of the user (write-only).

    Methods:
        validate: Ensures that passwords match and email is unique.
        create: Creates a new User instance and associated Token.
    """
        
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'fullname',
            'email',
            'password',
            'repeated_password'
        ]

    def validate(self, data):
        """
        Validate that passwords match and email is unique.

        Args:
            data (dict): Input data containing 'email', 'password', 'repeated_password'.

        Returns:
            dict: Validated data if checks pass.

        Raises:
            serializers.ValidationError: If passwords do not match or email exists.
        """
                
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'Email already exists.'})
        return data

    def create(self, validated_data):
        """
        Create a new User instance and associated authentication Token.

        Args:
            validated_data (dict): Validated user data.

        Returns:
            User: Newly created User instance.
        """
                
        validated_data.pop('repeated_password')
        fullname = validated_data.pop('fullname').strip()

        parts = fullname.split(' ', 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''

        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )

        Token.objects.create(user=user)

        return user

 