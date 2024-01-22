import requests
import logging

class GlobalService:
    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger(__name__)

    def generate_request(self, url, params={}, body_data={}):
        token = self.request.session.get('token')
        headers = {'Authorization': f'Token {token}'} if token else {}

        try:
            if body_data:
                response = requests.put(url, headers=headers, params=params, json=body_data)
            else:
                response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Error in API request: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.logger.error(f"Exception in API request: {e}")
            return None
