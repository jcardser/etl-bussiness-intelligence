import pandas as pd
from pathlib import Path
import math

class ExcelClient:
    """Cliente para leer y escribir archivos Excel usando pandas."""

    def read_excel(self, ruta: str) -> pd.DataFrame:
        """Lee un archivo Excel y devuelve un DataFrame."""
        try:
            df = pd.read_excel(ruta)
            print(f"✅ Archivo Excel leído correctamente: {ruta}")
            return df
        except Exception as e:
            print(f"❌ Error leyendo Excel: {e}")
            return pd.DataFrame()

    def export_to_excel(self, data, ruta: str, sheet_name: str = "Sheet1"):
        """
        Exporta un objeto (DataFrame o lista de diccionarios) a Excel.

        Args:
            data: pd.DataFrame | list[dict] → Datos a exportar.
            ruta: str → Ruta destino (por ejemplo, 'output/resultados.xlsx').
            sheet_name: str → Nombre de la hoja.
        """
        try:
            # Convertir a DataFrame si no lo es
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, pd.DataFrame):
                df = data
            else:
                raise TypeError("Solo se pueden exportar DataFrames o listas de diccionarios.")

            # Crear carpeta si no existe
            Path(ruta).parent.mkdir(parents=True, exist_ok=True)

            # Exportar
            df.to_excel(ruta, index=False, sheet_name=sheet_name)
            print(f"📊 Archivo Excel exportado exitosamente: {ruta}")

        except Exception as e:
            print(f"❌ Error exportando a Excel: {e}")


    def export_to_excel_per_pages(self, df: pd.DataFrame, ruta: str, sheet_name="Sheet", max_rows=1_048_000):
        """
        Exporta un DataFrame a Excel dividiéndolo en varias hojas si excede el límite.
        """
        try:
            total_rows = len(df)
            num_sheets = math.ceil(total_rows / max_rows)
            print(f"📄 Exportando {total_rows:,} filas en {num_sheets} hoja(s)...")

            with pd.ExcelWriter(ruta, engine="xlsxwriter") as writer:
                for i in range(num_sheets):
                    start_row = i * max_rows
                    end_row = min(start_row + max_rows, total_rows)
                    chunk = df.iloc[start_row:end_row]

                    sheet_name = f"{sheet_name}_{i+1}"
                    chunk.to_excel(writer, sheet_name=sheet_name, index=False)

            print(f"✅ Exportación completada en '{ruta}'.")

        except Exception as e:
            print(f"❌ Error exportando a Excel: {e}")
