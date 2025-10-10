from infrastructure.clients.excel_client import ExcelClient

class ETLPipeline:
    def __init__(self, extract_service, transform_service, xls_extract, load_service, collection_name: str, rename_map: dict = None):
        self.extract_service = extract_service
        self.xls_extract = xls_extract
        self.transform_service = transform_service
        self.load_service = load_service
        self.collection_name = collection_name
        self.rename_map = rename_map or {}

    def run(self):
        print("🚀 Iniciando pipeline ETL desde MongoDB...")
        df_raw = self.extract_service.extract(self.collection_name, query={}, limit=100)
        # df_clean = self.transform_service.clean_reviews(df_raw)
        # self.load_service.load_dataframe(df_raw, self.collection_name, self.rename_map)
        self.xls_extract.save_to_output(df_raw)
        print("✅ Pipeline ETL completado.")
