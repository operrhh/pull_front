import requests

class GlobalService:
    def __init__(self):
        None

    def generate_request(self, url, params={}, body_data={}):
        if body_data:
            try:
                response = requests.put(url, params=params, json=body_data)
                if response.status_code == 200:
                    return response.json()
                else:
                    return response.json()
            except Exception as e:
                return e
        else:
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    return response.json()
                else:
                    return response.json()
            except Exception as e:
                return e