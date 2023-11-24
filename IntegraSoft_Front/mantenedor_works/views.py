from django.shortcuts import render
from mantenedor_works.services.hcm.worker_service_hcm import WorkerServiceHcm
from mantenedor_works.services.peoplesoft.worker_service_peoplesoft import WorkerServicePeopleSoft

def index(request):
    return render(request, 'mantenedor_works/index_usuarios.html')

def get_worker_service(base_datos, request):
    if base_datos == 'HCM':
        return WorkerServiceHcm(request)
    elif base_datos == 'PeopleSoft':
        return WorkerServicePeopleSoft(request)
    else:
        raise ValueError("Base de datos no soportada")

def buscar_usuarios(request):
    usuarios = []
    name = ""  
    person_number = ""  
    base_datos = ""  

    if request.method == 'POST':
        base_datos = request.POST.get('base_datos', '')
        name = request.POST.get('name', '')
        person_number = request.POST.get('person_number', '')

        try:
            worker_service = get_worker_service(base_datos, request)
            # Asegúrate de que el método se llama correctamente
            usuarios = worker_service.buscar_usuarios_por_nombre(name, person_number)
        except ValueError as e:
            pass

    return render(request, 'mantenedor_works/buscar_usuarios.html', {
        'usuarios': usuarios, 
        'name': name, 
        'person_number': person_number,
        'base_datos': base_datos
    })
