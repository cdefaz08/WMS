# api_client.py

import requests
from config import API_BASE_URL

class APIClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def get(self, endpoint: str, **kwargs):
        return requests.get(f"{API_BASE_URL}{endpoint}", headers=self.headers, **kwargs)

    def post(self, endpoint: str, data=None, json=None, **kwargs):
        return requests.post(f"{API_BASE_URL}{endpoint}", headers=self.headers, data=data, json=json, **kwargs)

    def put(self, endpoint: str, data=None, json=None, **kwargs):
        return requests.put(f"{API_BASE_URL}{endpoint}", headers=self.headers, data=data, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return requests.delete(f"{API_BASE_URL}{endpoint}", headers=self.headers, **kwargs)
