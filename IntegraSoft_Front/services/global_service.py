import requests

class GlobalService:
    def __init__(self, request):
        self.request = request

    def generate_request(self, url, params={}, body_data={}):
        # Obtener el token de la sesión
        token = self.request.session.get('token')
        headers = {'Authorization': f'Token {token}'} if token else {}

        try:
            if body_data:
                response = requests.put(url, headers=headers, params=params, json=body_data)
            else:
                response = requests.get(url, headers=headers, params=params)
                print(response.url)

            if response.status_code == 200:
                return response.json()
            else:
                return response.json()
        except Exception as e:
            return e
