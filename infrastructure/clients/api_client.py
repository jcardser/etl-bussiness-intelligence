import requests
import pandas as pd

class APIClient:
    def read_api(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return pd.DataFrame(data)
        except requests.exceptions.RequestException as e:
            print(f"Error al llamar API: {e}")
            return None
