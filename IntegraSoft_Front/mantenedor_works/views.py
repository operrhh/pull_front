import logging
import requests 
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from mantenedor_works.services.hcm.worker_service_hcm import WorkerServiceHcm
from mantenedor_works.services.peoplesoft.worker_service_peoplesoft import WorkerServicePeopleSoft
from mantenedor_works.services.department.department import DepartmentService
from Decorators.auth_decorator import token_auth
from var.global_vars import resultados_hcm, resultados_peoplesoft
from django.urls import reverse
from IntegraSoft_Front import settings

logger = logging.getLogger(__name__)
@token_auth
def index(request):
    user = request.session['user']
    return render(request, 'mantenedor_works/index_usuarios.html',{'user': user, 'api_base_url': settings.API_BASE_URL})

def proxy_to_departments(request):
    base_datos = request.GET.get('base_datos', 'hcm')
    service = DepartmentService(request)
    departments = service.get_departments(base_datos)
    return JsonResponse({'departments': departments})

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
    firstName = ""
    lastName = ""  
    personNumber = ""  
    departamentoId = ""
    base_datos = ""  
    user = request.session.get('user', {})
    error_message = None  # Inicializa una variable para el mensaje de error

    if request.method == 'POST':
        firstName = request.POST.get('firstName', '')
        lastName = request.POST.get('lastName', '')
        personNumber = request.POST.get('personNumber', '')
        departamentoId = request.POST.get('departamento', '')
        base_datos = request.POST.get('base_datos', '')

        # Verifica si se ha seleccionado una base de datos
        if not base_datos:
            error_message = 'Debe seleccionar una base de datos.'

        # Verifica si todos los campos de búsqueda están vacíos y si se ha seleccionado una base de datos
        elif not (firstName or lastName or personNumber or departamentoId):
            error_message = 'Debe llenar al menos un campo para la búsqueda.'

        # Si no hay errores, procede con la búsqueda
        if not error_message:
            parametros = {'firstName': firstName, 'lastName': lastName, 'personNumber': personNumber}
            if departamentoId:
                parametros['department'] = departamentoId

            try:
                worker_service = get_worker_service(base_datos, request)
                if base_datos == 'HCM':
                    resultados_hcm = worker_service.buscar_usuarios_por_nombre(**parametros)
                elif base_datos == 'PeopleSoft':
                    resultados_peoplesoft = worker_service.buscar_usuarios_por_nombre(**parametros)
            except ValueError as e:
                logger.error(f"Error al buscar usuarios: {e}")
                error_message = "Ocurrió un error al buscar usuarios."

    return render(request, 'mantenedor_works/buscar_usuarios.html', {
        'path': request.path,
        'usuarios': resultados_hcm if base_datos == 'HCM' else resultados_peoplesoft,
        'firstName': firstName,
        'lastName': lastName,
        'personNumber': personNumber,
        'departamentoId': departamentoId,
        'base_datos': base_datos,
        'api_base_url': settings.API_BASE_URL,
        'user': user,
        'error_message': error_message  # Pasa el mensaje de error a la plantilla
    })


# views.py
@token_auth
def detalles_usuario(request, base_datos, user_id):
    user = request.session['user']

    detalles_hcm = None
    detalles_peoplesoft = None

    # Inicializa los servicios
    service_hcm = WorkerServiceHcm(request)
    service_peoplesoft = WorkerServicePeopleSoft(request)

    # Realiza la consulta principal y la consulta adicional a la otra base de datos
    if base_datos == 'HCM':
        detalles_hcm = service_hcm.get_worker(user_id)
        # Consulta adicional a PeopleSoft para obtener datos complementarios
        detalles_peoplesoft = service_peoplesoft.get_detalle_usuario_peoplesoft(user_id)
    elif base_datos == 'PeopleSoft':
        detalles_peoplesoft = service_peoplesoft.get_detalle_usuario_peoplesoft(user_id)
        # Consulta adicional a HCM para obtener datos complementarios
        detalles_hcm = service_hcm.get_worker(user_id)
    
    # Maneja el caso en que no se encuentren los detalles
    if detalles_hcm is None and detalles_peoplesoft is None:
        mensaje_error = 'Usuario no encontrado en ninguna de las bases de datos'
        return render(request, 'error.html', {'mensaje': mensaje_error})
    
    diferencias = comparar_datos(detalles_hcm, detalles_peoplesoft)
    print("Diferencias pasadas a la plantilla:", diferencias)
    # Pasa los detalles a la plantilla
    return render(request, 'mantenedor_works/hcm_peoplesoft.html', {
        'user': user,
        'base_datos': base_datos,
        'detalles_hcm': detalles_hcm,
        'detalles_peoplesoft': detalles_peoplesoft,
        'diferencias': diferencias
    })

def comparar_datos(detalles_hcm, detalles_peoplesoft):
    diferencias = {}
    mapeo_campos = {
        'person_number': 'emplid',
        'date_of_birth': 'birthdate',
        'display_name': 'name',
        'last_name': 'last_name',
        'first_name': 'first_name',
        'middle_names': 'middle_name',
        'country': 'country',
        'addressLine1': 'address1',
        'addressLine2': 'address2',
        'town_or_city': 'city',
        'system_person_type': 'per_org',
        'effective_start_date': 'hire_dt',
        'business_unit_name': 'business_unit',
        'ccu_codigo_centro_costo': 'deptid',
        'department_name': 'dept_descr',
        'job_code': 'jobcode',
        'standard_working_hours': 'std_hours',
        'locationCode': 'location',
        'managerAssignmentNumber': 'supervisor_id',
        'email_address': 'email'
    }

    for campo_hcm, campo_ps in mapeo_campos.items():
        if detalles_hcm.get(campo_hcm, '') != detalles_peoplesoft.get(campo_ps, ''):
            diferencias[campo_ps] = True

    # print("Diferencias encontradas:", diferencias)  # Añade esta línea
    return diferencias

