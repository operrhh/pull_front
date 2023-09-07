from django.shortcuts import render, redirect
from modelos.models.persona import Persona
from django.views import View
from django.core.paginator import Paginator

def index(request):
    lista_usuarios = Persona.objects.all()

    return render(request, 'mantenedor_works/index_usuarios.html', {

    })

# Funcion para definir usuarios
def buscar_usuarios(request):
    if request.method == 'GET':
        person_number = request.GET.get('person_number')
        nombre = request.GET.get('nombre')
        apellidos = request.GET.get('apellidos')
        ciudad = request.GET.get('ciudad')
        base_datos = request.GET.get('base_datos')

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
            if (not person_number or dato['person_number'] == person_number) and \
                    (not nombre or dato['nombre'].lower() == nombre.lower()) and \
                    (not apellidos or dato['apellidos'].lower() == apellidos.lower()) and \
                    (not ciudad or dato['ciudad'].lower() == ciudad.lower()):
                res.append(dato)

        # Obtener la página actual desde la URL o la variable de sesión
        registros_por_pagina = 7
        pagina_actual = request.GET.get('page')

        # Crear un objeto Paginator para dividir los resultados filtrados en páginas
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

    return render(request, 'mantenedor_works/index_usuarios.html')



# Mantén dos conjuntos de datos separados
def Cargar_resultados_PeopleSoft():
    # Datos de prueba para PeopleSoft
    datos_prueba_peoplesoft = [
        {'person_number': '001', 'nombre': 'Juan', 'apellidos': 'Pérez', 'ciudad': 'Madrid', 'edad': 20, 'renta' : 1000, 'unidad_negocio':'CCU'},
        {'person_number': '002', 'nombre': 'María', 'apellidos': 'Gómez', 'ciudad': 'Barcelona', 'edad': 30, 'renta' : 2000},
        {'person_number': '003', 'nombre': 'Carlos', 'apellidos': 'López', 'ciudad': 'Madrid', 'edad' : 40, 'renta' : 3000},
        {'person_number': '004', 'nombre': 'Carlor', 'apellidos': 'Lopez', 'ciudad': 'Madrid', 'edad': 50, 'renta' : 4000},
        {'person_number': '005', 'nombre': 'Carlor', 'apellidos': 'Sanchez', 'ciudad': 'Tijuana', 'edad': 60, 'renta' : 5000},
        {'person_number': '006', 'nombre': 'Carlor', 'apellidos': 'Sanchez', 'ciudad': 'Tijuana', 'edad': 70, 'renta' : 6000},
        {'person_number': '007', 'nombre': 'Juan', 'apellidos': 'Pérez', 'ciudad': 'Tijuana', 'edad': 80, 'renta' : 7000},
        {'person_number': '008', 'nombre': 'Juan', 'apellidos': 'Pérez', 'ciudad': 'Tijuana', 'edad': 90, 'renta' : 8000},
        {'person_number': '010', 'nombre': 'Juan', 'apellidos': 'Pérez', 'ciudad': 'Tijuana', 'edad': 90, 'renta' : 8000},
        {'person_number': '011', 'nombre': 'Juan', 'apellidos': 'Rodríguez', 'ciudad': 'Sevilla', 'edad': 35, 'renta': 2500},
        {'person_number': '012', 'nombre': 'Juan', 'apellidos': 'Martínez', 'ciudad': 'Madrid', 'edad': 28, 'renta': 1800},
        {'person_number': '013', 'nombre': 'Juan', 'apellidos': 'García', 'ciudad': 'Barcelona', 'edad': 32, 'renta': 2200},
        {'person_number': '014', 'nombre': 'Juan', 'apellidos': 'López', 'ciudad': 'Madrid', 'edad': 29, 'renta': 1900},
        {'person_number': '015', 'nombre': 'Juan', 'apellidos': 'Hernández', 'ciudad': 'Valencia', 'edad': 27, 'renta': 1700},
        {'person_number': '016', 'nombre': 'Juan', 'apellidos': 'Pérez', 'ciudad': 'Barcelona', 'edad': 40, 'renta': 3000},
        {'person_number': '017', 'nombre': 'Juan', 'apellidos': 'Gómez', 'ciudad': 'Madrid', 'edad': 50, 'renta': 4000},
        {'person_number': '018', 'nombre': 'Juan', 'apellidos': 'González', 'ciudad': 'Valencia', 'edad': 22, 'renta': 1300},
        {'person_number': '019', 'nombre': 'Juan', 'apellidos': 'Sánchez', 'ciudad': 'Sevilla', 'edad': 33, 'renta': 2300},
        {'person_number': '020', 'nombre': 'Juan', 'apellidos': 'Fernández', 'ciudad': 'Madrid', 'edad': 45, 'renta': 3500},
        {'person_number': '021', 'nombre': 'Juan', 'apellidos': 'Rodríguez', 'ciudad': 'Barcelona', 'edad': 38, 'renta': 2700},
        {'person_number': '022', 'nombre': 'Juan', 'apellidos': 'Martínez', 'ciudad': 'Valencia', 'edad': 31, 'renta': 2100},
        {'person_number': '023', 'nombre': 'Juan', 'apellidos': 'García', 'ciudad': 'Sevilla', 'edad': 42, 'renta': 3200},
        {'person_number': '024', 'nombre': 'Juan', 'apellidos': 'López', 'ciudad': 'Madrid', 'edad': 34, 'renta': 2400},
        {'person_number': '025', 'nombre': 'Juan', 'apellidos': 'Hernández', 'ciudad': 'Valencia', 'edad': 29, 'renta': 1900},
        {'person_number': '026', 'nombre': 'Juan', 'apellidos': 'Pérez', 'ciudad': 'Barcelona', 'edad': 48, 'renta': 3800},
        {'person_number': '027', 'nombre': 'Juan', 'apellidos': 'Gómez', 'ciudad': 'Madrid', 'edad': 41, 'renta': 3100},
        {'person_number': '028', 'nombre': 'Juan', 'apellidos': 'González', 'ciudad': 'Valencia', 'edad': 30, 'renta': 2000},
        {'person_number': '029', 'nombre': 'Juan', 'apellidos': 'Sánchez', 'ciudad': 'Sevilla', 'edad': 37, 'renta': 2600},


    ]
    return datos_prueba_peoplesoft

def Cargar_resultados_HCM():
    # Datos de prueba para HCM
    datos_prueba_hcm = [
        {'person_number': '001', 'nombre': 'Juan', 'apellidos': 'Pérez', 'ciudad': 'Madrid', 'edad': 20, 'renta' : 1000,'unidad_negocio':''},
        {'person_number': '002', 'nombre': 'María', 'apellidos': 'Gómez', 'ciudad': 'Barcelona', 'edad': 30, 'renta' : 2000},
        {'person_number': '003', 'nombre': 'Carlos', 'apellidos': 'López', 'ciudad': 'Madrid', 'edad' : 40, 'renta' : 3000},
        {'person_number': '004', 'nombre': 'Carlor', 'apellidos': 'Lopez', 'ciudad': 'Madrid', 'edad': 50, 'renta' : 4000},
        {'person_number': '005', 'nombre': 'Carlor', 'apellidos': 'Sanchez', 'ciudad': 'Tijuana', 'edad': 60, 'renta' : 5000},
        {'person_number': '006', 'nombre': 'Carlor', 'apellidos': 'Sanchez', 'ciudad': 'Tijuana', 'edad': 70, 'renta' : 6000},
        {'person_number': '007', 'nombre': 'Juan', 'apellidos': 'Pérez', 'ciudad': 'Tijuana', 'edad': 80, 'renta' : 7000},
        {'person_number': '008', 'nombre': 'Juan', 'apellidos': 'Pérez', 'ciudad': 'Tijuana', 'edad': 90, 'renta' : 8000},
        {'person_number': '009', 'nombre': 'Juan', 'apellidos': 'Pérez', 'ciudad': 'Tijuana', 'edad': 90, 'renta' : 8000},
    ]
    return datos_prueba_hcm

# Función para obtener un usuario por su ID

def obtener_usuario(user_id):
    datos_prueba_peoplesoft = Cargar_resultados_PeopleSoft()
    datos_prueba_hcm = Cargar_resultados_HCM()
    # Convertir user_id en cadena para comparación
    user_id = str(user_id)

    # Inicializar usuario como None en caso de no encontrar al usuario
    usuario = None

    # Buscar al usuario en los datos de PeopleSoft
    for dato in datos_prueba_peoplesoft:
        if dato['person_number'] == user_id:
            usuario = dato
            break  # Salir del bucle si el usuario se encuentra

    # Si no se encontró en PeopleSoft, buscar en los datos de HCM
    if not usuario:
        for dato in datos_prueba_hcm:
            if dato['person_number'] == user_id:
                usuario = dato
                break  # Salir del bucle si el usuario se encuentra

    return usuario

#Funcion para mostrar detalles de usuario en la grilla de detalles_usuario
def detalles_usuario(request, base_datos, user_id):
    # Determinar la fuente de datos según la selección del usuario
    datos_prueba_peoplesoft = Cargar_resultados_PeopleSoft()
    datos_prueba_hcm = Cargar_resultados_HCM()

    # Convertir user_id en cadena para comparación
    user_id = str(user_id)
    usuario = obtener_usuario(user_id)

    # Inicializar usuario como None en caso de no encontrar al usuario
    usuario_peoplesoft = []
    usuario_hcm = []
    
    # Buscar al usuario en los datos de PeopleSoft
    for dato in datos_prueba_peoplesoft:
        if dato['person_number'] == user_id:
            usuario_peoplesoft.append(dato)
            break  # Salir del bucle si el usuario se encuentra

    # Buscar al usuario en los datos de HCM
    for dato in datos_prueba_hcm:
        if dato['person_number'] == user_id:
            usuario_hcm.append(dato)
            break  # Salir del bucle si el usuario se encuentra

    print("Usuario PeopleSoft:", usuario_peoplesoft)  # Agregamos un print para verificar
    print("Usuario HCM:", usuario_hcm)

    # Verificar si se encontró al usuario en PeopleSoft o HCM
    if not usuario_peoplesoft and not usuario_hcm:
        print("Usuario no encontrado en los datos de prueba")  # Agregar un mensaje de depuración
        return render(request, 'mantenedor_works/error.html', {'error_message': 'Usuario no encontrado'})
    
    if usuario: 
     return render(
        request,
        'mantenedor_works/detalles_usuario.html',
        {
            'usuarios_peoplesoft': usuario_peoplesoft,
            'usuarios_hcm': usuario_hcm,
            'base_datos': base_datos,
            'usuario': usuario,
        }
    )

