from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Aqui, 'username' pode ser o e-mail que o usuário fornece
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
