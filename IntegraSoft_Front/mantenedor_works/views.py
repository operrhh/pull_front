import logging
from django.shortcuts import render, get_object_or_404
from mantenedor_works.services.hcm.worker_service_hcm import WorkerServiceHcm
from mantenedor_works.services.peoplesoft.worker_service_peoplesoft import WorkerServicePeopleSoft
from Decorators.auth_decorator import token_auth
from var.global_vars import resultados_hcm, resultados_peoplesoft

logger = logging.getLogger(__name__)
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
@token_auth
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
            'path': request.path,
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
@token_auth
def detalles_usuario(request, base_datos, user_id):
    global resultados_hcm, resultados_peoplesoft
    user = request.session['user']

    detalles_hcm = None
    detalles_peoplesoft = None

    # Si se selecciona PeopleSoft
    if base_datos == 'PeopleSoft':
        # Obtener detalles de PeopleSoft de la lista
        detalles_peoplesoft = next((usuario for usuario in resultados_peoplesoft if usuario['personNumber'] == user_id), None)
        
        # Consultar a HCM para obtener detalles
        service_hcm = WorkerServiceHcm(request)
        detalles_hcm = service_hcm.get_worker(user_id)

    # Si se selecciona HCM
    elif base_datos == 'HCM':
        # Obtener detalles de HCM de la lista
        detalles_hcm = next((usuario for usuario in resultados_hcm if usuario['personNumber'] == user_id), None)
        
        # Consultar a PeopleSoft para obtener detalles
        service_peoplesoft = WorkerServicePeopleSoft(request)
        detalles_peoplesoft = service_peoplesoft.get_worker(user_id)

    # Manejar casos en que no se encuentran los detalles
    if detalles_hcm is None or detalles_peoplesoft is None:
        return render(request, 'error.html', {'mensaje': 'Usuario no encontrado en las bases de datos seleccionadas'})
    print(detalles_hcm)
    print(detalles_peoplesoft)

    return render(request, 'mantenedor_works/hcm_peoplesoft.html', {
        'user': user,  # Usuario logueado
        'base_datos': base_datos,
        'detalles_hcm': detalles_hcm,
        'detalles_peoplesoft': detalles_peoplesoft
    })
