# auth_app/backends.py
from django.contrib.auth.models import User

class EmailAuthBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        # DRF übergibt das Feld als 'username', also prüfen wir auf email
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
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
