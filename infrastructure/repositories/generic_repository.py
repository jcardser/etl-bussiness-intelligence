import pandas as pd
from bson import ObjectId
from loguru import logger
from infrastructure.clients.mongo_client import MongoDBClient

class GenericRepository:
    def __init__(self, mongo_client: MongoDBClient):
        self.mongo_client = mongo_client
        self.logger = logger.bind(context="Repository")
        self.logger.info("Repository inicializado correctamente.")

    def read_collection(
        self,
        collection_name: str,
        query: dict = None,
        projection: dict = None,
        limit: int = 0
    ) -> pd.DataFrame:
        try:
            separator = "=" * 70
            self.logger.info(separator)
            self.logger.info("Mongo ETL - Leyendo datos desde MongoDB")
            self.logger.info(f"Leyendo colección '{collection_name}'...")
            collection = self.mongo_client.get_collection(collection_name)
            
            if collection is None:
                self.logger.error(f"No se pudo acceder a la colección '{collection_name}'.")
                return pd.DataFrame()

            cursor = collection.find(query or {}, projection or {})

            if limit > 0:
                cursor = cursor.limit(limit)
                self.logger.debug(f"Aplicado límite: {limit}")

            documents = list(cursor)

            if not documents:
                self.logger.warning(f"No se encontraron documentos en '{collection_name}'.")
                return pd.DataFrame()

            for doc in documents:
                if "_id" in doc and isinstance(doc["_id"], ObjectId):
                    doc["_id"] = str(doc["_id"])

            df = pd.DataFrame(documents)
            self.logger.success(f"Extraídos {len(df)} documentos desde '{collection_name}'.")
            return df

        except Exception as e:
            self.logger.exception(f"Error al leer la colección '{collection_name}': {e}")
            return pd.DataFrame()