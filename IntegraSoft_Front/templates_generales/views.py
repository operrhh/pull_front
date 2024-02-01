import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from IntegraSoft_Front.settings import API_BASE_URL
from Decorators.auth_decorator import token_auth
from django.utils import timezone
def login_view(request):
    # Verifica si el usuario ya está autenticado
    if 'token' in request.session:
        # Si ya hay un token en la sesión, redirige al usuario a la página principal
        return redirect('accounts:index_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        # Realiza la solicitud de autenticación a tu API
        login_url = f"{API_BASE_URL}/login/"
        response = requests.post(login_url, json={'username': username, 'password': password})

        if response.status_code == 200:
            # El usuario está autenticado, guarda el token en la sesión
            token = response.json().get('token')
            request.session['token'] = token
            request.session['user'] = username
            request.session.save()
            # Redirige a la página principal
            return redirect('accounts:index_home')
        else:
            # Si el login falla, muestra un mensaje de error
            messages.error(request, 'Proporcionó credenciales incorrectas, intentelo de nuevo por favor.')
    # Renderiza la plantilla de login si no es una solicitud POST o si el login falla
    return render(request, 'templates_generales/login.html')

@token_auth
def home_view(request):
    # Esta es la vista protegida que solo los usuarios autenticados pueden ver
    user = request.session['user']
    return render(request, 'templates_generales/home.html',{'user': user})

def logout_view(request):
    # Elimina toda la sesión
    request.session.flush()

    # Redirige al usuario a la página de inicio de sesión
    return redirect('accounts:login')

#validacion de usuario conectado antes de pasar al index