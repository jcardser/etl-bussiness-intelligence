import pandas as pd

class CSVClient:
    def read_csv(self, ruta, separador=","):
        try:
            return pd.read_csv(ruta, sep=separador)
        except Exception as e:
            print(f"Error leyendo CSV: {e}")
            return None
