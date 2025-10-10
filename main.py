from infrastructure.clients.mongo_client import MongoDBClient
from infrastructure.clients.postgres_client import PostgresClient
from infrastructure.repositories.generic_repository import GenericRepository
from infrastructure.loaders.postgres_loaders import PostgresLoaderService
from infrastructure.extractors.mongo_extractor import MongoExtractor
from infrastructure.clients.excel_client import ExcelClient
from infrastructure.extractors.xls_extractor import ExcelExtractor
from application.etl_pipeline import ETLPipeline
from infrastructure.setup_logger import setup_logging

if __name__ == "__main__":
    # Inicializar clientes
    logger = setup_logging()
    mongo_client = MongoDBClient("mongodb://localhost:27017", "airbnb")
    postgres_client = PostgresClient("admin", "admin123", "localhost", 5432, "mydb")
    excel_client = ExcelClient()
    excel_extractor = ExcelExtractor(excel_client)
    loader_postgres = PostgresLoaderService(postgres_client)

    rename_map_reviews = {
        "_id": "mongo_id",
        "id": "review_id",
        "date": "review_date"
    }
    
    rename_map_calendar = {
        "_id": "mongo_id",
    }

    repo = GenericRepository(mongo_client)
    extractor = MongoExtractor(repo)

    # ETLPipeline(extractor, {}, loader_postgres, "calendar", rename_map_calendar).run()
    # ETLPipeline(extractor, {}, loader_postgres, "reviews", rename_map_reviews).run()
    ETLPipeline(extractor, {}, excel_extractor, loader_postgres, "listings").run()


