from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'repeated_password']

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'Email already exists.'})
        return data

    def create(self, validated_data):
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

 