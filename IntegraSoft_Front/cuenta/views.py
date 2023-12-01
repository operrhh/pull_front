from django.shortcuts import render
from Decorators.auth_decorator import token_auth
# Create your views here.
@token_auth
def index(request):
    user = request.session['user']
    return render(request, 'cuenta/cuenta.html', {'user': user
    })