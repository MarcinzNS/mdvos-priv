from django.contrib.auth.backends import ModelBackend
from ..models.models import User

# używana przy logowaniu za pomocą adresu email

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None