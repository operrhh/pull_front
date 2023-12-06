from django.shortcuts import render, get_object_or_404
from mantenedor_works.services.hcm.worker_service_hcm import WorkerServiceHcm
from mantenedor_works.services.peoplesoft.worker_service_peoplesoft import WorkerServicePeopleSoft
from Decorators.auth_decorator import token_auth


@token_auth
def index(request):
    user = request.session['user']
    return render(request, 'mantenedor_works/index_usuarios.html',{'user': user})

def get_worker_service(base_datos, request):
    if base_datos == 'HCM':
        return WorkerServiceHcm(request)
    elif base_datos == 'PeopleSoft':
        return WorkerServicePeopleSoft(request)
    else:
        raise ValueError("Base de datos no soportada")

def buscar_usuarios(request):
    usuarios = []
    firstName = ""
    lastName = ""  
    personNumber = ""  
    base_datos = ""  
    user = request.session.get('user', {})  # Obtener usuario de la sesión

    if request.method == 'POST':
        base_datos = request.POST.get('base_datos', '')
        firstName = request.POST.get('firstName', '')
        lastName = request.POST.get('lastName', '')
        personNumber = request.POST.get('personNumber', '')

        try:
            worker_service = get_worker_service(base_datos, request)
            usuarios = worker_service.buscar_usuarios_por_nombre(firstName, lastName, personNumber)
        except ValueError as e:
            # Manejar el error si es necesario
            pass

    return render(request, 'mantenedor_works/buscar_usuarios.html', {
        'usuarios': usuarios, 
        'firstName': firstName,
        'lastName': lastName, 
        'personNumber': personNumber,
        'base_datos': base_datos,
        'user': user  # Usuario logueado
    })

def obtener_detalles_usuario(request, base_datos, user_id):
    if base_datos == 'HCM':
        service = WorkerServiceHcm(request)
    elif base_datos == 'PeopleSoft':
        service = WorkerServicePeopleSoft(request)
    else:
        return None

    return service.get_worker(user_id)

def detalles_usuario(request, base_datos, user_id):
    detalles = obtener_detalles_usuario(request, base_datos, user_id)

    if detalles is None:
        # Manejar el caso en que no se encuentren los detalles
        return render(request, 'error.html', {'mensaje': 'Usuario no encontrado'})

    return render(request, 'mantenedor_works/detalles_usuario.html', {'detalles': detalles})