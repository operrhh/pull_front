from django.shortcuts import render, redirect
from modelos.models.persona import Persona
from django.views import View
from django.core.paginator import Paginator
import json
from pathlib import Path

# Definir la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Función para cargar datos desde un archivo JSON
def cargar_datos_desde_json(archivo):
    with open(BASE_DIR / 'mantenedor_works' / 'datos_prueba' / archivo, 'r') as file:
        return json.load(file)

def index(request):
    lista_usuarios = Persona.objects.all()
    return render(request, 'mantenedor_works/index_usuarios.html', {})

def buscar_usuarios(request):
    pagina_actual = request.GET.get('page')
    
    if not pagina_actual:  # Si no hay número de página, es una nueva búsqueda
        # Obtener criterios de búsqueda de la solicitud
        person_number = request.GET.get('Person_Number')
        nombre = request.GET.get('nombre')
        business_unit_name = request.GET.get('BusinessUnitName')
        legislation_code = request.GET.get('LegislationCode')
        base_datos = request.GET.get('base_datos')
        
        # Almacenar criterios en la sesión
        request.session['Person_Number'] = person_number
        request.session['nombre'] = nombre
        request.session['BusinessUnitName'] = business_unit_name
        request.session['LegislationCode'] = legislation_code
        request.session['base_datos'] = base_datos
    else:  # Si hay un número de página, recuperar criterios de la sesión
        person_number = request.session.get('Person_Number')
        nombre = request.session.get('nombre')
        business_unit_name = request.session.get('BusinessUnitName')
        legislation_code = request.session.get('LegislationCode')
        base_datos = request.session.get('base_datos')

    # Identificar campos vacíos
    campos_vacios = []
    if not person_number:
        campos_vacios.append('Person_Number')
    if not nombre:
        campos_vacios.append('nombre')
    if not business_unit_name:
        campos_vacios.append('BusinessUnitName')
    if not legislation_code:
        campos_vacios.append('LegislationCode')

    # Verificar si todos los campos de filtro están vacíos
    if not any([person_number, nombre, business_unit_name, legislation_code]):
        contexto = {
            'error_message': 'Por favor, ingrese al menos un criterio de búsqueda.',
            'formulario_data': request.GET,
            'campos_vacios': campos_vacios  # Enviar la lista de campos vacíos al template
        }
        return render(request, 'mantenedor_works/buscar_usuarios.html', contexto)

    # Según la base de datos seleccionada, carga los resultados correspondientes
    if base_datos == 'PeopleSoft':
        resultados = Cargar_resultados_PeopleSoft()
    elif base_datos == 'HCM':
        resultados = Cargar_resultados_HCM()
    else:
        resultados = []

    # Aplicar filtros de búsqueda
    res = []
    for dato in resultados:
        first_name = dato['names'][0]['FirstName'].lower()
        last_name = dato['names'][0]['LastName'].lower()
        full_name = f"{first_name} {last_name}"  # Concatenar FirstName y LastName
        if (not person_number or dato['PersonNumber'] == person_number) and \
                (not nombre or nombre.lower() in first_name or nombre.lower() in last_name or nombre.lower() in full_name) and \
                (not business_unit_name or dato['workRelationships'][0]['assignments'][0]['BusinessUnitName'].lower() == business_unit_name.lower()) and \
                (not legislation_code or dato['names'][0]['LegislationCode'] == legislation_code):
            res.append(dato)

    # Crear un objeto Paginator para dividir los resultados filtrados en páginas
    registros_por_pagina = 7
    paginator = Paginator(res, registros_por_pagina)

    # Obtener la página actual de registros
    registros_pagina = paginator.get_page(pagina_actual)

    # Pasar los datos del formulario a la plantilla
    contexto = {
        'resultados': res,  # Pasamos los resultados filtrados
        'registros_pagina': registros_pagina,  # Pasamos los resultados paginados
        'formulario_data': request.GET,
    }

    return render(request, 'mantenedor_works/buscar_usuarios.html', contexto)


# Datos de prueba para PeopleSoft
def Cargar_resultados_PeopleSoft():
    # Por el momento tenemos los archivos en datos_prueba_peoplesoft.json
    return cargar_datos_desde_json('datos_prueba_peoplesoft.json')


# Datos de prueba para HCM
def Cargar_resultados_HCM():
    # Por el momento tenemos los archivos en datos_prueba_hcm.json
    return cargar_datos_desde_json('datos_prueba_hcm.json')


# Función para obtener un usuario por su ID
def obtener_usuario(user_id):
    datos_prueba_peoplesoft = Cargar_resultados_PeopleSoft()
    datos_prueba_hcm = Cargar_resultados_HCM()
    user_id = str(user_id)
    usuario = None

    for dato in datos_prueba_peoplesoft:
        if dato['PersonNumber'] == user_id:
            usuario = dato
            break

    if not usuario:
        for dato in datos_prueba_hcm:
            if dato['PersonNumber'] == user_id:
                usuario = dato
                break

    return usuario
# Funcion para mostrar detalles de usuario en la grilla de detalles_usuario
def detalles_usuario(request, base_datos, user_id):
    datos_prueba_peoplesoft = Cargar_resultados_PeopleSoft()
    datos_prueba_hcm = Cargar_resultados_HCM()
    
    # Convertir user_id en cadena para comparación
    user_id = str(user_id)
    usuario = obtener_usuario(user_id)
    
    usuario_peoplesoft = []
    usuario_hcm = []
    
    # Buscar al usuario en los datos de PeopleSoft
    for dato in datos_prueba_peoplesoft:
        if dato['PersonNumber'] == user_id:
            usuario_peoplesoft.append(dato)
            break  # Salir del bucle si el usuario se encuentra

    # Buscar al usuario en los datos de HCM
    for dato in datos_prueba_hcm:
        if dato['PersonNumber'] == user_id:
            usuario_hcm.append(dato)
            break  # Salir del bucle si el usuario se encuentra

    # Verificar si se encontró al usuario en PeopleSoft o HCM
    if not usuario:
        return render(request, 'mantenedor_works/error.html', {'error_message': 'Usuario no encontrado'})

    return render(
        request,
        'mantenedor_works/hcm_peoplesoft.html',
        {
            'usuarios_peoplesoft': usuario_peoplesoft,
            'usuarios_hcm': usuario_hcm,
            'usuario': usuario,
        }
    )

