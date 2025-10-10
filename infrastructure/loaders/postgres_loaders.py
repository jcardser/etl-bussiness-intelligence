import pandas as pd
from loguru import logger
from sqlalchemy import inspect
from infrastructure.clients.postgres_client import PostgresClient

# Configurar logger para este servicio


class PostgresLoaderService:
    """Servicio genérico para cargar DataFrames en tablas PostgreSQL."""

    def __init__(self, postgres_client: PostgresClient):
        self.postgres_client = postgres_client
        self.logger = logger.bind(context="PostgresClient")
        self.logger.info("🐘 PostgresLoaderService inicializado correctamente.")

    def load_dataframe(
        self,
        df: pd.DataFrame,
        table_name: str,
        rename_map: dict = None,
        if_exists: str = "append"
    ):
        """
        Inserta un DataFrame en la tabla especificada, validando columnas y registrando logs.

        Args:
            df (pd.DataFrame): DataFrame con los datos a insertar.
            table_name (str): Nombre de la tabla destino en PostgreSQL.
            rename_map (dict, opcional): Mapeo de nombres de columnas {origen: destino}.
            if_exists (str, opcional): Acción si la tabla existe. Valores: 'append', 'replace', 'fail'.
        """
        if df.empty:
            self.logger.warning(f"⚠️ DataFrame vacío. No se insertarán datos en '{table_name}'.")
            return

        try:
            # Renombrar columnas si se especifica un mapa
            if rename_map:
                df = df.rename(columns=rename_map)
                self.logger.debug(f"🔄 Columnas renombradas según mapa: {rename_map}")

            engine = self.postgres_client.connect()
            inspector = inspect(engine)

            if not inspector.has_table(table_name):
                self.logger.error(f"❌ La tabla '{table_name}' no existe en la base de datos.")
                return

            # Obtener columnas válidas de la tabla destino
            valid_columns = [col["name"] for col in inspector.get_columns(table_name)]
            df = df[[col for col in df.columns if col in valid_columns]]

            if df.empty:
                self.logger.warning(f"⚠️ Ninguna columna válida coincide con la tabla '{table_name}'.")
                return

            # Insertar en PostgreSQL
            df.to_sql(table_name, engine, if_exists=if_exists, index=False)
            self.logger.success(f"✅ Insertados {len(df)} registros en '{table_name}' correctamente.")

        except Exception as e:
            self.logger.exception(f"💥 Error al insertar datos en la tabla '{table_name}': {e}")
