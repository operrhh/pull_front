from django.shortcuts import render
import requests
from mantenedor_works.services.worker_service_hcm import WorkerServiceHcm

def index(request):
    return render(request, 'mantenedor_works/index_usuarios.html')

def buscar_usuarios(request):
    worker_service = WorkerServiceHcm(request)
    usuarios = []
    if request.method == 'POST':
        name = request.POST.get('name')
        usuarios = worker_service.buscar_usuarios_por_nombre(name)
    return render(request, 'mantenedor_works/buscar_usuarios.html', {'usuarios': usuarios})
