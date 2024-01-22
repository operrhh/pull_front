import os
from services.global_service import GlobalService
from IntegraSoft_Front.settings import API_BASE_URL

class WorkerServicePeopleSoft:
    def __init__(self, request):
        self.url = f"{API_BASE_URL}/worker/peoplesoft/"
        self.global_service = GlobalService(request)

    def buscar_usuarios_por_nombre(self, firstName, lastName, personNumber=None, department=None):
        params = {}
        if firstName:
            params['firstName'] = firstName
        if lastName:
            params['lastName'] = lastName
        if personNumber:
            params['personNumber'] = personNumber
        if department:
            params['department'] = department  # Agregar el filtro de departamento

        response = self.global_service.generate_request(self.url, params=params)
        usuarios = []
        if response and 'results' in response:
            for user in response['results']:
                usuario = self._procesar_usuario_peoplesoft(user)
                usuarios.append(usuario)
        return usuarios


    def get_worker(self, personNumber):
        try:
            # Modifica la URL para incluir manyWorkers=false
            url = f"{API_BASE_URL}/worker/peoplesoft/?manyWorkers=false&personNumber={personNumber}"

            # Realizar la solicitud a la API
            response = self.global_service.generate_request(url)
            if response and 'results' in response:
                worker_data = response['results'][0] if response['results'] else None
                if worker_data:
                    # Procesa y devuelve los datos del trabajador
                    return self._procesar_usuario_peoplesoft(worker_data)
                else:
                    return None
            else:
                return None
        except ValueError as e:
            print(f"Error al decodificar JSON: {e}")
            return None

    def _procesar_usuario_peoplesoft(self, user):
        nombre_completo = f"{user.get('first_name', '')} {user.get('middle_name', '').strip()} {user.get('last_name', '')}".strip()
        return {
            'nombre_completo': nombre_completo,
            'personNumber': user.get('emplid', ''),
            'email': user.get('email', ''),
            'telefono': user.get('home_phone', ''),
            'direccion': user.get('address1', ''),
            'department_name': user.get('deptname', '')  # Campo agregado para el departamento
        }