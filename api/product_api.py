import requests

BASE_URL = "https://qa-mdashboard.dev.gokwik.in"

class ProductAPI:
    def __init__(self, token=None):
        self.headers = {
            "Authorization": f"Bearer {token}" if token else "",
            "Content-Type": "application/json"
        }

    def get_products(self):
        response = requests.get(f"{BASE_URL}/api/products", headers=self.headers)
        return response