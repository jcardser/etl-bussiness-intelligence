from loguru import logger
import os
from datetime import datetime
import pandas as pd
from domain.interfaces.services.extractor_interface import IExtractor


class ExcelExtractor(IExtractor):
    def __init__(self, excel_client, path_input=None):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.excel_client = excel_client
        self.logger = logger.bind(context="ExcelExtractor")
        self.path_input = path_input
        self.path_output = os.path.join(BASE_DIR, "output")
        os.makedirs( self.path_output, exist_ok=True)

    def extract(self, path):
        try:
            self.logger.info(f"Leyendo archivo Excel desde: {path}")
            df = pd.read_excel(path)
            self.logger.info(f"Archivo leído correctamente con {len(df)} filas.")
            return df
        except Exception as e:
            self.logger.error(f"Error al leer archivo Excel: {e}", exc_info=True)
            raise

    def save_to_output(self, data, file_name ='', sheet_name="Sheet1"):
        try:
            if not isinstance(data, (pd.DataFrame, list)):
                raise TypeError("El parámetro 'data' debe ser un DataFrame o lista de diccionarios")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.path_output, f"extracted_data_{file_name}_{timestamp}.xlsx")

            self.logger.info(f"Guardando datos en: {output_file}")
            self.excel_client.export_to_excel(data, output_file, sheet_name=sheet_name)
            self.logger.info(f"Archivo Excel guardado exitosamente: {output_file}")

            return output_file

        except Exception as e:
            self.logger.error(f"Error al guardar los datos: {e}", exc_info=True)
            raise