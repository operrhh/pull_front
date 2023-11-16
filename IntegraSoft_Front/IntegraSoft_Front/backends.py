import requests
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from IntegraSoft_Front.settings import API_BASE_URL

class TokenBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        login_url = f"{API_BASE_URL}/login/"
        response = requests.post(login_url, json={'username': username, 'password': password})

        if response.status_code == 200:
            token = response.json().get('token')
            user, created = User.objects.get_or_create(username=username)

            # Guarda el token en la sesión del usuario
            if request:
                request.session['token'] = token

            user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
