from tracemalloc import start
from infrastructure.extractors import xls_extractor
from domain.services.transformation_service import TransformationService
from infrastructure.clients.mongo_client import MongoDBClient
from infrastructure.clients.postgres_client import PostgresClient
from infrastructure.repositories.generic_repository import GenericRepository
from infrastructure.loaders.postgres_loaders import PostgresLoaderService
from infrastructure.extractors.mongo_extractor import MongoExtractor
from infrastructure.clients.excel_client import ExcelClient
from infrastructure.extractors.xls_extractor import ExcelExtractor
from application.etl_pipeline import ETLPipeline
from infrastructure.setup_logger import setup_logging
from loguru import logger


if __name__ == "__main__":
    # Configuración de logging
    logger = setup_logging()
    logger.info("🚀 Iniciando proceso ETL principal...")

    # Clientes y servicios
    mongo_client = MongoDBClient("mongodb://localhost:27017", "airbnb")
    postgres_client = PostgresClient("admin", "admin123", "localhost", 5432, "mydb")
    xls_client = ExcelClient()
    xls_extractor = ExcelExtractor(xls_client)
    transformation_service = TransformationService()
    loader_postgres = PostgresLoaderService(postgres_client)
    extractor = MongoExtractor(GenericRepository(mongo_client))

    # Mapa de renombramiento (opcional)
    rename_map = {"_id": "mongo_id"}

    postgres_client.drop_all_tables()

    # Crear pipeline estrella
    pipeline = ETLPipeline(
        extract_service=extractor,
        transform_service=transformation_service,
        load_service=loader_postgres,
        rename_map=rename_map
    )

    try:
        # Ejecutar pipeline estrella
        star_schema = pipeline.run_star_schema()
        
        for name, df_or_dict in star_schema.items():
            if isinstance(df_or_dict, dict):
                for sub_name, df in df_or_dict.items():
                    xls_extractor.save_to_output(df, f"{name}_{sub_name}")
            else:
                xls_extractor.save_to_output(df_or_dict, name)

    except Exception as e:
        logger.exception(f"Error ejecutando pipeline estrella: {e}")

    logger.success("🎯 Proceso ETL completo. Modelo estrella cargado correctamente.")