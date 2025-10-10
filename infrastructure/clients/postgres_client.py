from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger


class PostgresClient:
    """Cliente genérico para conexión a PostgreSQL usando SQLAlchemy con Loguru."""

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
        """Crea el motor de conexión (engine)."""
        try:
            conn_str = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
            self.engine = create_engine(conn_str)
            self.logger.success(f"✅ Conectado a PostgreSQL → {self.db_name}")
            return self.engine
        except SQLAlchemyError as e:
            self.logger.error(f"❌ Error al conectar a PostgreSQL: {e}")
            return None

    def execute_query(self, query: str):
        """Ejecuta una consulta SQL y devuelve los resultados."""
        if not self.engine:
            self.logger.warning("⚠️ No hay conexión activa. Intentando reconectar...")
            self.connect()

        try:
            with self.engine.connect() as connection:
                self.logger.info(f"📄 Ejecutando consulta: {query[:100]}...")  # truncado por seguridad
                result = connection.execute(text(query))
                rows = result.fetchall()
                self.logger.success(f"✅ Consulta ejecutada con {len(rows)} filas obtenidas.")
                return [dict(row._mapping) for row in rows]
        except SQLAlchemyError as e:
            self.logger.exception(f"❌ Error ejecutando la consulta: {e}")
            return []

    def execute_non_query(self, query: str):
        """Ejecuta una consulta de escritura (INSERT, UPDATE, DELETE)."""
        if not self.engine:
            self.logger.warning("⚠️ No hay conexión activa. Intentando reconectar...")
            self.connect()

        try:
            with self.engine.begin() as connection:
                self.logger.info(f"✏️ Ejecutando operación: {query[:100]}...")
                connection.execute(text(query))
                self.logger.success("✅ Consulta de escritura ejecutada correctamente.")
        except SQLAlchemyError as e:
            self.logger.exception(f"❌ Error ejecutando consulta de escritura: {e}")

    def close(self):
        """Cierra la conexión si existe."""
        if self.engine:
            self.engine.dispose()
            self.logger.info("🔒 Conexión a PostgreSQL cerrada correctamente.")
        else:
            self.logger.warning("⚠️ No había conexión activa para cerrar.")
