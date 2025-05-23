from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned

Account = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Account.objects.get(email=username)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None