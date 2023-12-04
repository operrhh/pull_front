import os
from services.global_service import GlobalService
from IntegraSoft_Front.settings import API_BASE_URL

class WorkerServicePeopleSoft:
    def __init__(self, request):
        self.url = f"{API_BASE_URL}/worker/peoplesoft/"
        self.global_service = GlobalService(request)

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
                usuario = self._procesar_usuario_peoplesoft(user)
                usuarios.append(usuario)
        return usuarios

    def get_worker_peoplesoft(self, emplid):
        response = self.global_service.generate_request(f"{self.url}?emplid={emplid}")
        if response and 'results' in response:
            for user in response['results']:
                if user.get('emplid') == emplid:
                    return self._procesar_usuario_peoplesoft(user)
        return "No se encontró el trabajador"

    def _procesar_usuario_peoplesoft(self, user):
        return {
            'nombre_completo': user.get('name', ''),   # SE DEBE CAMBIAR EL CAMPO DE BUSQUEDA POR FIRST NAME Y LAST NAME IGUAL QUE HCM
            'personNumber': user.get('emplid', ''),
            'email': user.get('email', ''),  # Asumiendo que hay un campo email
            'telefono': user.get('home_phone', ''),
            'direccion': user.get('address1', '')
            # Agrega más campos según sea necesario
        }
