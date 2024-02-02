import logging
import requests 
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from mantenedor_works.services.hcm.worker_service_hcm import WorkerServiceHcm
from mantenedor_works.services.peoplesoft.worker_service_peoplesoft import WorkerServicePeopleSoft
from mantenedor_works.services.department.department import DepartmentService
from Decorators.auth_decorator import token_auth
from urllib.parse import unquote
from django.urls import reverse
from IntegraSoft_Front import settings
from django.http import JsonResponse
from urllib.parse import unquote

logger = logging.getLogger(__name__)
@token_auth
def index(request):
    user = request.session['user']
    return render(request, 'mantenedor_works/index_usuarios.html',{'user': user, 'api_base_url': settings.API_BASE_URL})

@token_auth
def proxy_to_departments(request):
    base_datos = request.GET.get('base_datos', 'hcm')
    search = request.GET.get('name', '')  # Cambiado a 'name' para coincidir con el parámetro de la API

    service = DepartmentService(request)
    response = service.get_departments(base_datos, search_query=search)
    return JsonResponse(response)

def get_worker_service(base_datos, request):
    if base_datos == 'HCM':
        return WorkerServiceHcm(request)
    elif base_datos == 'PeopleSoft':
        return WorkerServicePeopleSoft(request)
    else:
        raise ValueError("Base de datos no soportada")
    


@token_auth
def buscar_usuarios(request):
    firstName = ""
    lastName = ""  
    personNumber = ""  
    departamentoId = ""
    base_datos = ""  
    user = request.session.get('user', {})
    error_message = None  
    resultados = []  # Lista para almacenar los resultados
    has_more = False
    next_url = None

    # Obtén el offset de la URL para HCM
    offset = request.GET.get('offset', None)

    if request.method == 'POST':
        firstName = request.POST.get('firstName', '')
        lastName = request.POST.get('lastName', '')
        personNumber = request.POST.get('personNumber', '')
        departamentoId = request.POST.get('departamento', '')
        base_datos = request.POST.get('base_datos', '')

        if not base_datos:
            error_message = 'Debe seleccionar una base de datos.'
        elif not (firstName or lastName or personNumber or departamentoId):
            error_message = 'Debe llenar al menos un campo para la búsqueda.'
        else:
            try:
                worker_service = get_worker_service(base_datos, request)
                if base_datos == 'HCM':
                    resultados_hcm = worker_service.buscar_usuarios_por_nombre(
                        firstName=firstName,
                        lastName=lastName,
                        personNumber=personNumber,
                        department=departamentoId,
                        offset=offset  # Usa el offset de la URL
                    )
                    # Extraemos la información de paginación si está presente
                    if resultados_hcm and isinstance(resultados_hcm[-1], dict) and 'has_more' in resultados_hcm[-1]:
                        has_more = resultados_hcm[-1]['has_more']
                        next_url = resultados_hcm[-1]['next_url']
                        resultados_hcm = resultados_hcm[:-1]  # Removemos el elemento de paginación
                    resultados = resultados_hcm

                elif base_datos == 'PeopleSoft':
                    response = worker_service.buscar_usuarios_por_nombre(
                        firstName=firstName,
                        lastName=lastName,
                        personNumber=personNumber,
                        department=departamentoId
                    )
                    if response:
                        resultados, has_more, next_url = response
                    else:
                        resultados, has_more, next_url = ([], False, None)  # Valores predeterminados en caso de None
                print("siguiente_url", next_url)

            except ValueError as e:
                logger.error(f"Error al buscar usuarios: {e}")
                error_message = "Ocurrió un error al buscar usuarios."

    return render(request, 'mantenedor_works/buscar_usuarios.html', {
        'path': request.path,
        'usuarios': resultados,
        'firstName': firstName,
        'lastName': lastName,
        'personNumber': personNumber,
        'departamentoId': departamentoId,
        'base_datos': base_datos,
        'api_base_url': settings.API_BASE_URL,
        'user': user,
        'error_message': error_message,
        'has_more': has_more,
        'next_url': next_url
    })

# views.py
# @token_auth
# def detalles_usuario(request, base_datos, user_id):
#     user = request.session.get('user', {})
#     detalles_hcm = None
#     detalles_peoplesoft = None
#     diferencias = {}  # Asegúrate de inicializar la variable diferencias

#     service_hcm = WorkerServiceHcm(request)
#     service_peoplesoft = WorkerServicePeopleSoft(request)

#     if base_datos == 'HCM':
#         detalles_hcm = service_hcm.get_worker(user_id)
#         detalles_peoplesoft = service_peoplesoft.get_detalle_usuario_peoplesoft(user_id)
        
#     elif base_datos == 'PeopleSoft':
#         detalles_peoplesoft = service_peoplesoft.get_detalle_usuario_peoplesoft(user_id)
#         detalles_hcm = service_hcm.get_worker(user_id)


#     if detalles_hcm or detalles_peoplesoft:
#         diferencias = comparar_datos(detalles_hcm, detalles_peoplesoft)
#         detalles_hcm['complete_name'] = detalles_hcm.get('complete_name', '').title()
#         detalles_peoplesoft['name'] = detalles_peoplesoft.get('name', '').title()    
       
       

#     # Agrega un mensaje si no se encuentran detalles
#     mensaje_hcm = 'No se encontraron datos en HCM para este usuario.' if not detalles_hcm else ''
#     mensaje_peoplesoft = 'No se encontraron datos en PeopleSoft para este usuario.' if not detalles_peoplesoft else ''

#     context = {
#         'user': user,
#         'base_datos': base_datos,
#         'detalles_hcm': detalles_hcm,
#         'detalles_peoplesoft': detalles_peoplesoft,
#         'diferencias': diferencias,
#         'mensaje_hcm': mensaje_hcm,
#         'mensaje_peoplesoft': mensaje_peoplesoft
#     }
    
   
#     return render(request, 'mantenedor_works/hcm_peoplesoft.html', context)

@token_auth
def detalles_usuario(request, base_datos, user_id):
    user = request.session.get('user', {})
    detalles_hcm = None
    detalles_peoplesoft = None
    diferencias = {}
    mensaje_hcm = ''
    mensaje_peoplesoft = ''

    service_hcm = WorkerServiceHcm(request)
    service_peoplesoft = WorkerServicePeopleSoft(request)

    if base_datos == 'HCM':
        detalles_hcm = service_hcm.get_worker(user_id)
        detalles_peoplesoft = service_peoplesoft.get_detalle_usuario_peoplesoft(user_id)
        mensaje_peoplesoft = 'No se encontraron datos en PeopleSoft para este usuario.' if not detalles_peoplesoft else ''
    elif base_datos == 'PeopleSoft':
        detalles_peoplesoft = service_peoplesoft.get_detalle_usuario_peoplesoft(user_id)
        detalles_hcm = service_hcm.get_worker(user_id)
        mensaje_hcm = 'No se encontraron datos en HCM para este usuario.' if not detalles_hcm else ''


    if detalles_hcm and detalles_peoplesoft:
        diferencias = comparar_datos(detalles_hcm, detalles_peoplesoft)
        detalles_hcm['complete_name'] = detalles_hcm.get('complete_name', '').title() if detalles_hcm else 'No disponible'
        detalles_peoplesoft['name'] = detalles_peoplesoft.get('name', '').title() if detalles_peoplesoft else 'No disponible'

    context = {
        'user': user,
        'base_datos': base_datos,
        'detalles_hcm': detalles_hcm,
        'detalles_peoplesoft': detalles_peoplesoft,
        'diferencias': diferencias,
        'mensaje_hcm': mensaje_hcm,
        'mensaje_peoplesoft': mensaje_peoplesoft
    }
    
    return render(request, 'mantenedor_works/hcm_peoplesoft.html', context)

def comparar_datos(detalles_hcm, detalles_peoplesoft):
    diferencias = {}
    mapeo_campos = {
        'complete_name':'name',
        'person_number': 'emplid',
        'date_of_birth': 'birthdate',
        'last_name': 'last_name',
        'first_name': 'first_name',
        'middle_names': 'middle_name',
        'legal_employer_code':'company',
        'country': 'country',
        'addressLine1': 'address1',
        'addressLine2': 'address2',
        'town_or_city': 'city',
        'system_person_type': 'per_org',
        'effective_start_date': 'hire_dt',
        'business_unit_name': 'business_unit',
        'business_unit_name': 'business_unit_descr',
        'ccu_codigo_centro_costo': 'deptid',
        'department_name': 'dept_descr',
        'job_code': 'jobcode',
        'standard_working_hours': 'std_hours',
        'locationCode': 'location',
        'managerAssignmentNumber': 'supervisor_id',
        'email_address': 'email'
    }

    for campo_hcm, campo_ps in mapeo_campos.items():
            # Comprobación de None antes de intentar llamar a .get()
            valor_hcm = detalles_hcm.get(campo_hcm, None) if detalles_hcm else None
            valor_ps = detalles_peoplesoft.get(campo_ps, None) if detalles_peoplesoft else None

            # Si ambos valores son iguales (o ambos None), no hay diferencia
            if valor_hcm == valor_ps:
                diferencias[campo_hcm] = False
            else:
                # Hay una diferencia si alguno de los valores es None, o si son diferentes
                diferencias[campo_hcm] = True

    return diferencias



@token_auth
def cargar_mas_usuarios(request):
    next_url = request.GET.get('next_url')
    base_datos = request.GET.get('base_datos', 'HCM')  # O un valor por defecto

    # Impresiones para depuración
    print("Base de datos seleccionada:", base_datos)
    print("URL siguiente:", next_url)

    if not next_url:
        return JsonResponse({'error': 'URL de próxima página no proporcionada'}, status=400)

    next_url = unquote(next_url)

    try:
        if base_datos == 'HCM':
            service = WorkerServiceHcm(request)
            response_data = service.get_worker_next(next_url)
        elif base_datos == 'PeopleSoft':
            service = WorkerServicePeopleSoft(request)
            response_data = service.get_worker_next_ps(next_url)
        else:
            return JsonResponse({'error': 'Base de datos no válida'}, status=400)

        # Imprimir la respuesta para depuración
        print("Datos de respuesta:", response_data)

        if response_data:
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Error al obtener más usuarios'}, status=500)

    except Exception as e:
        print(f"Error en cargar_mas_usuarios: {e}")
        return JsonResponse({'error': str(e)}, status=500)
