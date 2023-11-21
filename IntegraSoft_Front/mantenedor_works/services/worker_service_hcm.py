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

    def get_worker(self, pk):
        response = self.global_service.generate_request(f"{self.url}{pk}/")
        if response and 'results' in response:
            return response['results'][0]
        else:
            return "No se encontró el trabajador"

    def buscar_usuarios_por_nombre(self, name):
        params = {'name': name}
        response = self.global_service.generate_request(self.url, params=params)
        usuarios = []
        if response and 'results' in response:
            for user in response['results']:
                for name in user['names']:
                    usuario = {
                        'nombre_completo': f"{name.get('first_name', '').strip()} {name.get('last_name', '').strip()}",
                        'person_number': user.get('person_number', ''),
                        'email': user['emails'][0].get('email_address', '') if user['emails'] else '',
                        'telefono': user['phones'][0].get('phone_number', '') if user['phones'] else '',
                        'direccion': user['addresses'][0].get('addressLine1', '') if user['addresses'] else ''
                    }
                    usuarios.append(usuario)
        return usuarios
