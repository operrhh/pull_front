import os
from services.global_service import GlobalService
from IntegraSoft_Front.settings import API_BASE_URL

class WorkerServiceHcm:
    def __init__(self, request):
        self.url = f"{API_BASE_URL}/worker/hcm/"
        self.global_service = GlobalService(request)

    def get_workers(self, params={}):
        response = self.global_service.generate_request(self.url, params=params)
        if response and 'items' in response:
            return response['items']
        else:
            return "No se encontraron trabajadores"

    def get_worker(self, personNumber):
        try:
            url = f"{self.url}?personNumber={personNumber}&manyWorkers=false"
            response = self.global_service.generate_request(url)

            if response:
                return self._procesar_usuario_hcm(response)
            else:
                return None
        except Exception as e:
            print(f"Error al procesar la respuesta de la API: {e}")
            return None
    def _procesar_usuario_hcm(self, worker_data):
    # Asume que worker_data es un diccionario directamente desde el JSON
        nombres = worker_data.get('names', [])
        emails = worker_data.get('emails', [])
        telefonos = worker_data.get('phones', [])
        direcciones = worker_data.get('addresses', [])
        relaciones_laborales = worker_data.get('work_relationships', [])

        nombre_completo = nombres[0].get('display_name', '') if nombres else ''
        email = emails[0].get('email_address', '') if emails else ''
        telefono = telefonos[0].get('phone_number', '') if telefonos else ''
        direccion = direcciones[0].get('addressLine1', '') if direcciones else ''
        department_name = (relaciones_laborales[0].get('assignment', {}).get('department_name', '') 
                            if relaciones_laborales else '')

        return {
            'nombre_completo': nombre_completo,
            'personNumber': worker_data.get('person_number', ''),
            'email': email,
            'telefono': telefono,
            'direccion': direccion,
            'department_name': department_name
        }


    def _procesar_usuario_hcm(self, worker_data):
        # Procesamiento similar a PeopleSoft
        names = worker_data.get('names', [])
        emails = worker_data.get('emails', [])
        phones = worker_data.get('phones', [])
        addresses = worker_data.get('addresses', [])
        work_relationships = worker_data.get('work_relationships', [])

        nombre_completo = names[0].get('display_name', '') if names else ''
        email = emails[0].get('email_address', '') if emails else ''
        telefono = phones[0].get('phone_number', '') if phones else ''
        direccion = addresses[0].get('addressLine1', '') if addresses else ''
        department_name = (work_relationships[0].get('assignment', {}).get('department_name', '') 
                            if work_relationships else '')

        return {
            'nombre_completo': nombre_completo,
            'personNumber': worker_data.get('person_number', ''),
            'email': email,
            'telefono': telefono,
            'direccion': direccion,
            'department_name': department_name
        }

    def buscar_usuarios_por_nombre(self, firstName, lastName, personNumber=None, department=None):
        params = {}
        if firstName:
            params['firstName'] = firstName
        if lastName:
            params['lastName'] = lastName
        if personNumber:    
            params['personNumber'] = personNumber
        if department:
            params['department'] = department

        response = self.global_service.generate_request(self.url, params=params)
        usuarios = []
        if response and 'items' in response:
            for user in response['items']:
                usuario = {
                    'nombre_completo': user.get('display_name', ''),
                    'personNumber': user.get('person_number', ''),
                    'department_name': user.get('department_name', '')
                    # Aquí puedes agregar más campos si la API los proporciona
                }
                usuarios.append(usuario)
        return usuarios

    def _obtener_campo(self, lista, campo):
        if lista:
            for item in lista:
                if campo in item:
                    return item[campo]
        return ''
