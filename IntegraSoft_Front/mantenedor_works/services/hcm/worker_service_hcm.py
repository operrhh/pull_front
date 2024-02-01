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
        # Extracción de datos de las diferentes secciones
        nombres = worker_data.get('names', [])[0] if worker_data.get('names') else {}
        emails = worker_data.get('emails', [])[0] if worker_data.get('emails') else {}
        telefonos = worker_data.get('phones', [])[0] if worker_data.get('phones') else {}
        direcciones = worker_data.get('addresses', [])[0] if worker_data.get('addresses') else {}
        relaciones_laborales = worker_data.get('work_relationships', [])[0] if worker_data.get('work_relationships') else {}
        assignment = relaciones_laborales.get('assignment', {}) if relaciones_laborales else {}
        
        # Construcción del diccionario con los datos extraídos
        datos_procesados = {
            'person_number': worker_data.get('person_number', ''),
            'date_of_birth': worker_data.get('date_of_birth', ''),
            'legal_employer_code': relaciones_laborales.get('legal_employer_code', ''),
            'complete_name': nombres.get('complete_name', '').strip().upper(),
            'display_name': nombres.get('display_name', ''),
            'last_name': nombres.get('last_name', ''),
            'first_name': nombres.get('first_name', ''),
            'middle_names': nombres.get('middle_names', ''),
            'country': worker_data.get('country_of_birth', ''),
            'addressLine1': direcciones.get('addressLine1', ''),
            'addressLine2': direcciones.get('addressLine2', ''),
            'town_or_city': direcciones.get('town_or_city', ''),
            'system_person_type': assignment.get('system_person_type', ''),
            'salary_amount': assignment.get('salary_amount', ''),
            'effective_start_date': assignment.get('effective_start_date', ''),
            'business_unit_name': assignment.get('business_unit_name', ''),
            'ccu_codigo_centro_costo': assignment.get('ccu_codigo_centro_costo', ''),
            'department_name': assignment.get('department_name', ''),
            'job_code': assignment.get('job_code', ''),
            'standard_working_hours': assignment.get('standard_working_hours', ''),
            'locationCode': assignment.get('location_code', ''),
            'managerAssignmentNumber': assignment.get('manager', ''),
            'email_address': emails.get('email_address', ''),
            'telefono': telefonos.get('phone_number', '')
        }
        
        print(datos_procesados)
        return datos_procesados
    
    def buscar_usuarios_por_nombre(self, firstName, lastName, personNumber=None, department=None, offset=None):
        params = {
            'firstName': firstName,
            'lastName': lastName,
            'personNumber': personNumber,
            'department': department,
            'offset': offset
        }
        
        # Filtramos los parámetros para eliminar aquellos que sean None o estén vacíos
        params = {k: v for k, v in params.items() if v}

        response = self.global_service.generate_request(self.url, params=params)
        
        # Inicializamos usuarios como una lista vacía
        usuarios = []
        
        if response and 'items' in response:
            # Procesamos los usuarios normalmente
            for user in response['items']:
                usuarios.append({
                    'nombre_completo': user.get('display_name', ''),
                    'personNumber': user.get('person_number', ''),
                    'department_name': user.get('department_name', '')
                })
            
            # Verificamos si hay más páginas y la URL para la próxima carga
            if response.get('hasMore', False):
                usuarios.append({
                    'has_more': True,
                    'next_url': response.get('next')
                })   
        return usuarios

    def get_worker_next (self, url):
        response = self.global_service.generate_request(url)
        if response and 'items' in response:
            return response


      
