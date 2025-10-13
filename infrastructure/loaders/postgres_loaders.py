import pandas as pd
from loguru import logger
# from sqlalchemy import inspect
from infrastructure.clients.postgres_client import PostgresClient


class PostgresLoaderService:
    def __init__(self, postgres_client: PostgresClient):
        self.postgres_client = postgres_client
        self.logger = logger
        separator = "=" * 70
        self.logger.info(separator)
        self.logger.info("PostgresLoaderService inicializado correctamente.")

    def load_dataframe(
        self,
        df: pd.DataFrame,
        table_name: str,
        rename_map: dict = None,
        if_exists: str = "replace"
    ):
        if df.empty:
            self.logger.warning(
                f"DataFrame vacío. No se insertarán datos en '{table_name}'.")
            return

        try:
            if rename_map:
                df = df.rename(columns=rename_map)
                self.logger.debug(f"Columnas renombradas según mapa: {rename_map}")

            engine = self.postgres_client.connect()

            df.to_sql(table_name, engine, if_exists=if_exists, index=False)
            self.logger.success(f"Tabla '{table_name}' cargada con {len(df)} filas.")

        except Exception as e:
            self.logger.exception(f"Error al insertar datos en la tabla '{table_name}': {e}")
