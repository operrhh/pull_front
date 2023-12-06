from django.shortcuts import render, get_object_or_404
from mantenedor_works.services.hcm.worker_service_hcm import WorkerServiceHcm
from mantenedor_works.services.peoplesoft.worker_service_peoplesoft import WorkerServicePeopleSoft
from Decorators.auth_decorator import token_auth
from var.global_vars import resultados_hcm, resultados_peoplesoft

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
    global resultados_hcm, resultados_peoplesoft
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
                if base_datos == 'HCM':
                    resultados_hcm = worker_service.buscar_usuarios_por_nombre(firstName, lastName, personNumber)
                elif base_datos == 'PeopleSoft':
                    resultados_peoplesoft = worker_service.buscar_usuarios_por_nombre(firstName, lastName, personNumber)
            except ValueError as e:
                # Manejar el error si es necesario
                pass

    return render(request, 'mantenedor_works/buscar_usuarios.html', {
            'usuarios': resultados_hcm if base_datos == 'HCM' else resultados_peoplesoft, 
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

# views.py
def detalles_usuario(request, base_datos, user_id):
    global resultados_hcm, resultados_peoplesoft

    # Buscar detalles en HCM
    detalles_hcm = next((usuario for usuario in resultados_hcm if usuario['personNumber'] == user_id), None)

    # Si no se encuentra en HCM, mostrar error
    if detalles_hcm is None:
        return render(request, 'error.html', {'mensaje': 'Usuario no encontrado en HCM'})

    # Buscar detalles en PeopleSoft
    service_peoplesoft = WorkerServicePeopleSoft(request)
    detalles_peoplesoft = service_peoplesoft.get_worker(user_id)

    # Si no se encuentra en PeopleSoft, puedes decidir cómo manejarlo
    if detalles_peoplesoft is None:
        detalles_peoplesoft = {}  # O manejar de otra manera

    return render(request, 'mantenedor_works/hcm_peoplesoft.html', {
        'detalles_hcm': detalles_hcm,
        'detalles_peoplesoft': detalles_peoplesoft
    })
