import requests 
from django.conf import settings

def authenticate_user (request, username, password):
    login_url = f"{settings.API_BASE_URL}/login/"
    response = requests.post(login_url, json={'username': username, 'password': password})

    if response.status_code == 200:
        token = response.json().get('token')
        # Guarda el token en la sesión del usuario
        request.session['token'] = token
        request.session['user'] = username
        return True
    return False
