import os
from services.global_service import GlobalService
from IntegraSoft_Front.settings import API_BASE_URL

class DepartmentService:
    def __init__(self, request):
        self.global_service = GlobalService(request)

    def get_departments(self, base_datos):
        api_url = f"{API_BASE_URL}/department/{base_datos.lower()}/"
        response = self.global_service.generate_request(api_url)
        if response and 'items' in response:
            return response['items']
        else:
            return []