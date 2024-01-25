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
        
    def get_more_departments(self, base_datos, page=1, search_query=''):
        page_size = 50  # Define el número de resultados por página
        offset = (page - 1) * page_size
        api_url = f"{API_BASE_URL}/department/{base_datos.lower()}/?offset={offset}&limit={page_size}"

        if search_query:
            api_url += f"&search={search_query}"

        response = self.global_service.generate_request(api_url)
        if response:
            return response  # Devuelve la respuesta completa, incluyendo 'items', 'next', etc.
        else:
            return {"items": [], "hasMore": False}