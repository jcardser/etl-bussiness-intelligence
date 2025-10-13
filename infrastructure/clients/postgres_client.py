from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

class PostgresClient:
    def __init__(self, user: str, password: str, host: str, port: int, db_name: str):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.engine = None
        self.logger = logger.bind(context="Client")
        self.logger.info(f"Inicializando cliente PostgreSQL para BD: {db_name}")

    def connect(self):
        try:
            conn_str = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
            self.engine = create_engine(conn_str)
            self.logger.success(f"Conectado a PostgreSQL → {self.db_name}")
            return self.engine
        except SQLAlchemyError as e:
            self.logger.error(f"Error al conectar a PostgreSQL: {e}")
            return None

    def close(self):
        if self.engine:
            self.engine.dispose()
            self.logger.info("Conexión a PostgreSQL cerrada correctamente.")
        else:
            self.logger.warning("No había conexión activa para cerrar.")

    def drop_all_tables(self):
        if not self.engine:
            self.logger.warning("No hay conexión activa. Intentando reconectar...")
            self.connect()

        try:
            with self.engine.begin() as connection:
                tables = connection.execute(
                    text("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema='public' AND table_type='BASE TABLE';
                    """)
                ).fetchall()

                if not tables:
                    self.logger.info("No se encontraron tablas para eliminar.")
                    return

                for table in tables:
                    table_name = table[0]
                    self.logger.info(f"Eliminando tabla '{table_name}' con CASCADE...")
                    connection.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;'))
                    self.logger.success(f"Tabla '{table_name}' eliminada.")

        except SQLAlchemyError as e:
            self.logger.exception(f"Error eliminando tablas: {e}")
