import os
from services.global_service import GlobalService
from IntegraSoft_Front.settings import API_BASE_URL

class WorkerServiceHcm:
    def __init__(self, request):
        self.url = f"{API_BASE_URL}/worker/hcm/"
        self.global_service = GlobalService(request)

    def get_workers(self, params={}):
        response = self.global_service.generate_request(self.url, params=params)
        if response and 'results' in response:
            return response['results']
        else:
            return "No se encontraron trabajadores"

    def get_worker(self, personNumber):
            try:
                url = f"{self.url}?personNumber={personNumber}"
                response = self.global_service.generate_request(url)
                if response and 'results' in response:
                    # Procesar la respuesta para extraer los datos relevantes
                    worker_data = response['results'][0] if response['results'] else None
                    if worker_data:
                        return {
                            'nombre_completo': self._obtener_campo(worker_data.get('names', []), 'display_name'),
                            'personNumber': self._obtener_campo(worker_data.get('person_number', []), 'person_number'),
                            'email': self._obtener_campo(worker_data.get('emails', []), 'email_address'),
                            'telefono': self._obtener_campo(worker_data.get('phones', []), 'phone_number'),
                            'direccion': self._obtener_campo(worker_data.get('addresses', []), 'addressLine1')
                        }
                    else:
                        return None
                else:
                    return None
            except ValueError as e:
                print(f"Error al decodificar JSON: {e}")
                return None


    def buscar_usuarios_por_nombre(self, firstName, lastName, personNumber=None):
        params = {}
        if firstName:
            params['firstName'] = firstName
        if lastName:
            params['lastName'] = lastName
        if personNumber:    
            params['personNumber'] = personNumber

        response = self.global_service.generate_request(self.url, params=params)
        usuarios = []
        if response and 'results' in response:
            for user in response['results']:
                # Utiliza el campo full_name para el nombre completo
                nombre_completo = self._obtener_campo(user.get('names', []), 'display_name')

                email = self._obtener_campo(user.get('emails', []), 'email_address')
                telefono = self._obtener_campo(user.get('phones', []), 'phone_number')
                direccion = self._obtener_campo(user.get('addresses', []), 'addressLine1')

                usuario = {
                    'nombre_completo': nombre_completo,
                    'personNumber': user.get('person_number', ''),
                    'email': email,
                    'telefono': telefono,
                    'direccion': direccion
                }
                usuarios.append(usuario)
        return usuarios

    def _obtener_campo(self, lista, campo):
        if lista:
            for item in lista:
                if campo in item:
                    return item[campo]
        return ''
