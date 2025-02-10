from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try to authenticate by email first
        try:
            user = User.objects.get(email=username)  # Try to find user by email
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)  # Fallback to username if email doesn't match
            except User.DoesNotExist:
                return None
        
        if user and user.check_password(password):  # Check the password
            return user
        return None
