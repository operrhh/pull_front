import os
from services.global_service import GlobalService
from IntegraSoft_Front.settings import API_BASE_URL

class WorkerServicePeopleSoft:
    def __init__(self, request):
        self.url = f"{API_BASE_URL}/worker/peoplesoft/"
        self.global_service = GlobalService(request)
