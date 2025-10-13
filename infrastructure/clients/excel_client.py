import pandas as pd
from pathlib import Path
import math

class ExcelClient:
    def read_excel(self, ruta: str) -> pd.DataFrame:
        try:
            df = pd.read_excel(ruta)
            print(f"✅ Archivo Excel leído correctamente: {ruta}")
            return df
        except Exception as e:
            print(f"❌ Error leyendo Excel: {e}")
            return pd.DataFrame()

    def export_to_excel(self, data, ruta: str, sheet_name: str = "Sheet1"):
        try:
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, pd.DataFrame):
                df = data
            else:
                raise TypeError("Solo se pueden exportar DataFrames o listas de diccionarios.")

            Path(ruta).parent.mkdir(parents=True, exist_ok=True)

            df.to_excel(ruta, index=False, sheet_name=sheet_name)
            print(f"📊 Archivo Excel exportado exitosamente: {ruta}")

        except Exception as e:
            print(f"❌ Error exportando a Excel: {e}")