from django.shortcuts import render, redirect
from modelos.models.persona import Persona
from django.views import View
from django.core.paginator import Paginator
import json
from pathlib import Path
from django.http import JsonResponse
# -*- coding: utf-8 -*-
BASE_DIR = Path(__file__).resolve().parent.parent

def index(request):
    
    return render(request, 'mantenedor_works/index_usuarios.html', {})
       
def cargar_datos_desde_json(archivo):
    with open(BASE_DIR / 'mantenedor_works' / 'datos_prueba' / archivo, 'r', encoding='utf-8') as file:
        return json.load(file)


    
def obtener_opciones_por_base(request):
    base_datos = request.GET.get('base_datos')
    
    if base_datos not in ['PeopleSoft', 'HCM']:
        return JsonResponse({'error': 'Base de datos no válida'}, status=400)
    
    archivo = f'datos_prueba_{base_datos.lower()}.json'
    opciones_unidad_negocio = obtener_valores_unicos_desde_json([archivo], 'workRelationships', 'BusinessUnitName', 'assignments')
    opciones_departamento = obtener_valores_unicos_desde_json([archivo], 'workRelationships', 'DepartmentName', 'assignments')
    
    return JsonResponse({
        'opciones_unidad_negocio': opciones_unidad_negocio,
        'opciones_departamento': opciones_departamento,
    })
def obtener_valores_unicos_desde_json(archivos, campo_anidado_1, campo, campo_anidado_2=None):
    valores = set()
    
    for archivo in archivos:
        datos = cargar_datos_desde_json(archivo)
        
        # Asegurarse de que los datos son una lista
        if isinstance(datos, dict):
            datos = [datos]
        
        for dato in datos:
            for subdato in dato.get(campo_anidado_1, []):
                if campo_anidado_2:
                    for item in subdato.get(campo_anidado_2, []):
                        if campo in item:
                            valores.add(item[campo])
                else:
                    if campo in subdato:
                        valores.add(subdato[campo])
    return list(valores)


def buscar_usuarios(request):
    pagina_actual = request.GET.get('page')

    archivos = ['datos_prueba_hcm.json', 'datos_prueba_peoplesoft.json']  # Asume que tienes un archivo llamado 'datos_prueba_peoplesoft.json' para PeopleSoft
    opciones_unidad_negocio = obtener_valores_unicos_desde_json(archivos, 'workRelationships', 'BusinessUnitName', 'assignments')
    opciones_departamento = obtener_valores_unicos_desde_json(archivos, 'workRelationships', 'DepartmentName', 'assignments')

    if not pagina_actual:
        person_number = request.GET.get('Person_Number')
        nombre = request.GET.get('nombre')
        business_unit_name = request.GET.get('BusinessUnitName')
        department_name = request.GET.get('DepartmentName')
        base_datos = request.GET.get('base_datos')
        
        
        request.session['Person_Number'] = person_number
        request.session['nombre'] = nombre
        request.session['BusinessUnitName'] = business_unit_name
        request.session['DepartmentName'] = department_name
        request.session['base_datos'] = base_datos
        
    else:
        person_number = request.session.get('Person_Number')
        nombre = request.session.get('nombre')
        business_unit_name = request.session.get('BusinessUnitName')
        department_name = request.session.get('DepartmentName')
        base_datos = request.session.get('base_datos')
        

    campos_vacios = []
    if not person_number:
        campos_vacios.append('Person_Number')
    if not nombre:
        campos_vacios.append('nombre')
    if not business_unit_name:
        campos_vacios.append('BusinessUnitName')
  
    if not department_name:
        campos_vacios.append('DepartmentName')

    if not any([person_number, nombre, business_unit_name, department_name]):
        contexto = {
            'error_message': 'Por favor, ingrese al menos un criterio de búsqueda.',
            'formulario_data': request.GET,
            'campos_vacios': campos_vacios
        }
        return render(request, 'mantenedor_works/buscar_usuarios.html', contexto)
    
    if base_datos == 'PeopleSoft':
        resultados = cargar_resultados_peoplesoft()
    elif base_datos == 'HCM':
        resultados = cargar_resultados_hcm()
    else:
        resultados = []

    res = []
    for dato in resultados:
        first_name = dato['names'][0]['FirstName'].lower()
        last_name = dato['names'][0]['LastName'].lower()
        full_name = f"{first_name} {last_name}"
        business_unit = dato['workRelationships'][0]['assignments'][0]['BusinessUnitName'].lower()    
        department_from_data = dato['workRelationships'][0]['assignments'][0].get('DepartmentName', None)
        
        if (not person_number or dato['PersonNumber'] == person_number) and \
                (not nombre or nombre.lower() in first_name or nombre.lower() in last_name or nombre.lower() in full_name) and \
                (not business_unit_name or business_unit == business_unit_name.lower()) and \
                (not department_name or department_from_data == department_name):

                
            res.append(dato)

    registros_por_pagina = 7
    paginator = Paginator(res, registros_por_pagina)
    registros_pagina = paginator.get_page(pagina_actual)

    resultados_hcm = cargar_resultados_hcm()
    resultados_peoplesoft = cargar_resultados_peoplesoft()

    resultados_con_discrepancias = []
    for dato in resultados:
        usuario_hcm = next((user for user in resultados_hcm if user['PersonNumber'] == dato['PersonNumber']), None)
        usuario_peoplesoft = next((user for user in resultados_peoplesoft if user['PersonNumber'] == dato['PersonNumber']), None)

        discrepancias = contar_discrepancias([usuario_hcm] if usuario_hcm else [], [usuario_peoplesoft] if usuario_peoplesoft else [])
        resultados_con_discrepancias.append({
            'PersonNumber': dato['PersonNumber'],
            'discrepancias': discrepancias
        })



    contexto = {
        'resultados': res,
        'registros_pagina': registros_pagina,
        'formulario_data': request.GET,
        'opciones_unidad_negocio': opciones_unidad_negocio,
        'opciones_departamento': opciones_departamento,
        'resultados_con_discrepancias': resultados_con_discrepancias,
        
    }

    return render(request, 'mantenedor_works/buscar_usuarios.html', contexto)

# Datos de prueba para PeopleSoft
def cargar_resultados_peoplesoft():
    # Por el momento tenemos los archivos en datos_prueba_peoplesoft.json
    return cargar_datos_desde_json('datos_prueba_peoplesoft.json')


# Datos de prueba para HCM
def cargar_resultados_hcm():
    # Por el momento tenemos los archivos en datos_prueba_hcm.json
    return cargar_datos_desde_json('datos_prueba_hcm.json')


# Función para obtener un usuario por su ID
def obtener_usuario(user_id):
    datos_prueba_peoplesoft = cargar_resultados_peoplesoft()
    datos_prueba_hcm = cargar_resultados_hcm()
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
def contar_discrepancias(usuarios_hcm, usuarios_peoplesoft):
    conteo = 0

    if not (usuarios_hcm and usuarios_peoplesoft):
        return conteo

    if usuarios_hcm[0]['workRelationships'][0]['LegalEmployerName'] != usuarios_peoplesoft[0]['workRelationships'][0]['LegalEmployerName']:
        conteo += 1

    if usuarios_hcm[0]['workRelationships'][0]['assignments'][0]['BusinessUnitName'] != usuarios_peoplesoft[0]['workRelationships'][0]['assignments'][0]['BusinessUnitName']:
        conteo += 1

    # Aquí puedes agregar más condiciones y aumentar el conteo según sea necesario

    return conteo




def detalles_usuario(request, base_datos, user_id):
    datos_prueba_peoplesoft = cargar_resultados_peoplesoft()
    datos_prueba_hcm = cargar_resultados_hcm()
    
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

    numero_discrepancias = contar_discrepancias(usuario_hcm, usuario_peoplesoft)

    return render(
        request,
        'mantenedor_works/hcm_peoplesoft.html',
        {
            'usuarios_peoplesoft': usuario_peoplesoft,
            'usuarios_hcm': usuario_hcm,
            'usuario': usuario,
            'numero_discrepancias': numero_discrepancias,  # Pasa el número de discrepancias a la plantilla
            'formulario_data': {'base_datos': base_datos},
        }
    )


