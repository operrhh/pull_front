import os
from services.global_service import GlobalService
from IntegraSoft_Front.settings import API_BASE_URL

class WorkerServicePeopleSoft:
    def __init__(self, request):
        self.url = f"{API_BASE_URL}/worker/peoplesoft/"
        self.global_service = GlobalService(request)

    def buscar_usuarios_por_nombre(self, firstName, lastName, personNumber=None, department=None, offset=None):
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
        next_url = None
        if response and 'results' in response:
            for user in response['results']:
                usuario = self._procesar_usuario_peoplesoft(user)
                usuarios.append(usuario)
            next_url = response.get('next', None)
            has_more = bool(next_url)
            return usuarios, has_more, next_url


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

    def get_detalle_usuario_peoplesoft(self, personNumber):
        try:
            # Modifica la URL para incluir manyWorkers=false
            url = f"{self.url}?manyWorkers=false&personNumber={personNumber}"

            # Realizar la solicitud a la API
            response = self.global_service.generate_request(url)
            if response and 'results' in response:
                worker_data = response['results'][0] if response['results'] else None
                if worker_data:
                    # Procesa y devuelve los datos detallados del trabajador
                    return self._procesar_detalle_usuario_peoplesoft(worker_data)
                else:
                    return None
            else:
                return None
        except ValueError as e:
            print(f"Error al decodificar JSON: {e}")
            return None
    def _procesar_detalle_usuario_peoplesoft(self, user):

    # Concatenar los nombres con espacios entre ellos solo si el nombre respectivo no está vacío
       # Extraer todos los campos necesarios del usuario para los detalles completos
        return {
            'emplid': user.get('emplid', ''),
            'birthdate': user.get('birthdate', ''),
            'company': user.get('company', ''),
            'monthly_rt': user.get('monthly_rt', ''),
            'name': user.get('name', '').strip().upper(),
            'last_name': user.get('last_name', ''),
            'first_name': user.get('first_name', ''),
            'middle_name': user.get('middle_name', ''),
            'second_last_name': user.get('second_last_name', ''),
            'country': user.get('country', ''),
            'address1': user.get('address1', ''),
            'address2': user.get('address2', ''),
            'city': user.get('city', ''),
            'per_org': user.get('per_org', ''),
            'hire_dt': user.get('hire_dt', ''),
            'business_unit': user.get('business_unit', ''),
            'business_unit_descr': user.get('business_unit_descr', ''),
            'deptid': user.get('deptid', ''),
            'dept_descr': user.get('dept_descr', ''),
            'jobcode': user.get('jobcode', ''),
            'std_hours': user.get('std_hours', ''),
            'location': user.get('location', ''),
            'supervisor_id': user.get('supervisor_id', ''),
            'email': user.get('email', ''),
            'telefono': user.get('home_phone', ''),
            'department_name': user.get('deptname', '')
        }
    
    def get_worker_next_ps(self, url):
        try:
            response = self.global_service.generate_request(url)
            print("respuesta_next", response)

            if response and 'results' in response:
                # Procesa la respuesta como sea necesario
                return response
            else:
                print("No se encontraron 'results' en la respuesta")
                return None
        except Exception as e:
            print(f"Error al realizar la solicitud a la API: {e}")
            return None