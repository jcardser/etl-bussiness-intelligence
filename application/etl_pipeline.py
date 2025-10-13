from loguru import logger
from infrastructure.extractors.mongo_extractor import MongoExtractor
from infrastructure.loaders.postgres_loaders import PostgresLoaderService
from domain.services.transformation_service import TransformationService

class ETLPipeline:
    def __init__(self, extract_service, transform_service, load_service, rename_map: dict = None):
        self.extract_service: MongoExtractor = extract_service
        self.transform_service: TransformationService = transform_service
        self.load_service:PostgresLoaderService = load_service
        self.rename_map = rename_map or {}
        self.logger = logger

    def run_star_schema(self):
        self.logger.info("=" * 70)
        self.logger.info("Iniciando ETL analítico (modelo estrella)...")

        # === Extraer ===
        df_listings_raw = self.extract_service.extract("listings", {}, limit=100)
        df_calendar_raw = self.extract_service.extract("calendar", {}, limit=100)
        df_reviews_raw = self.extract_service.extract("reviews", {}, limit=100)

        if df_listings_raw.empty or df_calendar_raw.empty or df_reviews_raw.empty:
            self.logger.error("Faltan colecciones requeridas para generar el modelo estrella.")
            return

        # === Transformar ===
        df_combined = self.transform_service._transform_listings_and_hosts(df_listings_raw)
        df_hosts = df_combined["hosts"]
        df_listings = df_combined["listings"]
        df_calendar = self.transform_service._clean_calendar(df_calendar_raw)
        df_reviews_result = self.transform_service._clean_reviews(df_reviews_raw)

        # === Generar dimensiones y hechos ===
        star_schema = self.transform_service.build_star_schema(
            df_listings=df_listings,
            df_hosts=df_hosts,
            df_reviews_result=df_reviews_result,
            df_calendar=df_calendar
        )

        # === Cargar en PostgreSQL ===
        self.logger.info("Cargando dimensiones...")
        for name, df in {k: v for k, v in star_schema.items() if k.startswith("dim_")}.items():
            self.load_service.load_dataframe(df, name, self.rename_map)
            self.logger.success(f"Dimensión '{name}' cargada ({len(df)} filas).")

        self.logger.info("Cargando hechos...")
        self.load_service.load_dataframe(star_schema["fact_calendar"], "fact_calendar", self.rename_map)
        self.load_service.load_dataframe(star_schema["fact_reviews"], "fact_reviews", self.rename_map)

        self.logger.success("Modelo estrella cargado correctamente en PostgreSQL.")
        return {
            "df_listings":df_listings,
            "df_hosts":df_hosts,
            "df_reviews_result":df_reviews_result,
            "df_calendar":df_calendar
        }