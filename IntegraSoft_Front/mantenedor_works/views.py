from django.shortcuts import render
from modelos.models.work import Work
# Create your views here.
def index(request):
    lista_usuarios= Work.objects.all()
    return render(request, 'mantenedor_works/usuarios.html', {
        'lista_usuarios': lista_usuarios 
    })