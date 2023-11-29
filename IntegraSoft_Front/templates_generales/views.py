# views.py
import logging
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from IntegraSoft_Front.settings import API_BASE_URL
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Decorators import auth_decorator

@auth_decorator.token_auth
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "templates_generales/home.html"

# views.py

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # El usuario está autenticado, inicia la sesión
            login(request, user)
            # Redirige a la página principal
            return redirect('index_home')
        else:
            # Si el login falla, muestra un mensaje de error
            messages.error(request, 'Login fallido. Por favor, intenta de nuevo.')
#prueba
    # Renderiza la plantilla de login si no es una solicitud POST o si el login falla
    return render(request, 'templates_generales/login.html')
