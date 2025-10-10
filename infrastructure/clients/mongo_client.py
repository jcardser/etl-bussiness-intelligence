from loguru import logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

class MongoDBClient:
    """Cliente genérico para conexión a MongoDB con Loguru."""

    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None
        self.logger = logger.bind(context="Client")
        self.logger.info(f"Inicializando cliente MongoDB para: {db_name}")

    def connect(self):
        """Conecta al servidor de MongoDB y valida conexión."""
        try:
            self.logger.info(f"Intentando conectar a MongoDB → {self.uri}/{self.db_name}")
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.db.list_collection_names()
            self.logger.success(f"✅ Conexión exitosa a MongoDB → {self.db_name}")
            return self.db
        except ConnectionFailure as e:
            self.logger.error(f"❌ Error de conexión: {e}")
            return None
        except PyMongoError as e:
            self.logger.exception(f"⚠️ Error inesperado: {e}")
            return None

    def get_collection(self, name: str):
        """Obtiene una colección."""
        if self.db is None:
            self.logger.warning("⚠️ Base de datos no conectada, intentando reconectar...")
            self.connect()
        if self.db is not None:
            self.logger.info(f"📂 Accediendo a colección: {name}")
            return self.db[name]
        else:
            self.logger.error(f"❌ No se pudo acceder a la colección: {name}")
            return None

    def close(self):
        """Cierra la conexión."""
        if self.client:
            self.client.close()
            self.logger.info("🔒 Conexión MongoDB cerrada correctamente.")
        else:
            self.logger.warning("⚠️ Intento de cerrar una conexión inexistente.")
