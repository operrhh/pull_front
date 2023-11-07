import requests

from ...services.global_service import GlobalService


class WorkerServiceHcm:
    def __init__(self):
        self.url = "http://127.0.0.1:8000/worker/hcm/"

        self.global_service = GlobalService()

    def get_workers(self):
        response = self.global_service.generate_request(self.url)
        if response:
            if response.get('count') > 0:
                return response.json()['results']
            else:
                return "No se encontró el trabajador"
        else:
            return response.json()

    def get_worker(self, pk):
        response = requests.get(self.url + str(pk) + "/")
        response = self.global_service.generate_request(self.url, params={'pk': pk})

        if response:
            if response.get('count') > 0:
                return response.json()['results'][0]
            else:
                return "No se encontró el trabajador"
        else:
            return response.json()
        