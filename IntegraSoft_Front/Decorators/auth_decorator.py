from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect, render

def token_auth(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Aquí implementas tu lógica de verificación de autenticación.
        # Por ejemplo, puedes verificar si hay un token en la sesión:
        if 'token' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            # Si el usuario no está autenticado, puedes redirigirlo o mostrar un error
            return redirect('accounts:login')

    return _wrapped_view

