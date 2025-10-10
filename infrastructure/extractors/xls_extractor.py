# infrastructure/extractors/excel_extractor.py

from loguru import logger
import os
from datetime import datetime
import pandas as pd
from domain.interfaces.services.extractor_interface import IExtractor


class ExcelExtractor(IExtractor):
    def __init__(self, excel_client):
        self.excel_client = excel_client
        self.logger = logger.bind(context="ExcelExtractor")
        # Asegurar carpeta de salida
        os.makedirs("output", exist_ok=True)


    def extract(self, path):
        try:
            self.logger.info(f"Leyendo archivo Excel desde: {path}")
            df = pd.read_excel(path)
            self.logger.info(
                f"Archivo leído correctamente con {len(df)} filas.")
            return df
        except Exception as e:
            self.logger.error(
                f"Error al leer archivo Excel: {e}", exc_info=True)
            raise
    def save_to_output(self, data, filename="extracted_data.xlsx", sheet_name="Sheet1"):
        """
        Guarda un DataFrame o lista de diccionarios en la carpeta de salida (output/),
        agregando timestamp al nombre del archivo.
        """
        try:
            # Validación de tipo
            if not isinstance(data, (pd.DataFrame, list)):
                raise TypeError("El parámetro 'data' debe ser un DataFrame o lista de diccionarios")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(filename)[0]
            output_file = os.path.join("output", f"{base_name}_{timestamp}.xlsx")

            self.logger.info(f"Guardando datos en: {output_file}")
            self.excel_client.export_to_excel(data, output_file, sheet_name=sheet_name)
            self.logger.info(f"Archivo Excel guardado exitosamente: {output_file}")

            return output_file

        except Exception as e:
            self.logger.error(f"Error al guardar los datos: {e}", exc_info=True)
            raise