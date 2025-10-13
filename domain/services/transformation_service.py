from loguru import logger
import pandas as pd
from itertools import chain

class TransformationService:
    def __init__(self):
        self.logger = logger

    def _transform_hosts(self, df: pd.DataFrame) -> pd.DataFrame:
        hosts_cols = [
            "host_id", "host_url", "host_name", "host_since", "host_location",
            "host_about", "host_response_time", "host_response_rate",
            "host_acceptance_rate", "host_is_superhost", "host_thumbnail_url",
            "host_picture_url", "host_neighbourhood", "host_listings_count",
            "host_total_listings_count", "host_verifications",
            "host_has_profile_pic", "host_identity_verified"
        ]
        df_hosts = df[hosts_cols].drop_duplicates(subset=["host_id"]).copy()

        # Tipos y limpieza
        df_hosts["host_since"] = pd.to_datetime(df_hosts["host_since"], errors="coerce")
        df_hosts["host_is_superhost"] = df_hosts["host_is_superhost"].astype(bool)
        df_hosts["host_has_profile_pic"] = df_hosts["host_has_profile_pic"].astype(bool)
        df_hosts["host_identity_verified"] = df_hosts["host_identity_verified"].astype(bool)


        df_hosts["host_verifications"] = (
            df_hosts["host_verifications"]
            .astype(str)
            .str.replace(r"[\[\]']", "", regex=True)
            .str.lower()
            .str.split(r"[,;]\s*")
        )

        # Columnas booleanas por verificación
        all_verifications = set(chain.from_iterable(
            v for v in df_hosts["host_verifications"] if isinstance(v, list)
        ))
        for verif in all_verifications:
            col_name = f"has_{verif}_verification"
            df_hosts[col_name] = df_hosts["host_verifications"].apply(
                lambda x: verif in x if isinstance(x, list) else False
            )

        df_hosts.drop(columns=["host_verifications"], inplace=True)
        df_hosts = self.drop_irrelevant_columns(df_hosts, "hosts")
        self.logger.info(f"Transformados {len(df_hosts)} hosts con {len(all_verifications)} verificaciones únicas.")
        return df_hosts

    def _transform_listings(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforma la información de los listings."""
        # Conservar host_id aunque demás columnas host_ se eliminen
        listings_cols = [col for col in df.columns if not col.startswith("host_") or col == "host_id"]
        df_listings = df[listings_cols].copy()
    
        # Limpieza de precios
        df_listings["price"] = (
            df_listings["price"].astype(str).str.replace(r"[^0-9.]", "", regex=True)
        )
        df_listings["price"] = pd.to_numeric(df_listings["price"], errors="coerce").fillna(0)
    
        # Limpieza de fechas
        date_cols = ["last_scraped", "calendar_last_scraped", "first_review", "last_review"]
        for col in date_cols:
            if col in df_listings.columns:
                df_listings[col] = pd.to_datetime(df_listings[col], errors="coerce")
    
        df_listings = self.drop_irrelevant_columns(df_listings, "listings")
        self.logger.info(f"Transformados {len(df_listings)} listings.")
        return df_listings


    def _transform_listings_and_hosts(self, df: pd.DataFrame) -> dict:
        """Transforma simultáneamente los datos de hosts y listings."""
        df_hosts = self._transform_hosts(df)
        df_listings = self._transform_listings(df)
        return {"hosts": df_hosts, "listings": df_listings}

    def _clean_calendar(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["price"] = (
            df["price"].astype(str).str.replace(r"[^0-9.]", "", regex=True).astype(float)
        ).fillna(0)
        df["available"] = df["available"].astype(bool)
        self.logger.info(f"Transformados {len(df)} registros de calendar.")
        return df

    def _clean_reviews(self, df: pd.DataFrame) -> dict:
        df = df.copy()
        df["comments"] = df["comments"].fillna("").str.strip()
        df["reviewer_name"] = df["reviewer_name"].fillna("Unknown")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        df_guests = df[["reviewer_id", "reviewer_name"]].drop_duplicates()
        df_reviews = df[["listing_id", "reviewer_id", "comments", "date"]].copy()
        self.logger.info(f"Transformados {len(df_reviews)} reviews y {len(df_guests)} guests.")
        return {"reviews": df_reviews, "guests": df_guests}

    # ---------------------------
    # Dimensiones y hechos
    # ---------------------------
    def drop_irrelevant_columns(self, df: pd.DataFrame, collection_name: str) -> pd.DataFrame:
        drop_columns = {
            "listings": [
                "listing_url", "source", "description", "neighborhood_overview",
                "picture_url", "host_url", "host_thumbnail_url", "host_picture_url",
                "host_about", "bathrooms_text", "minimum_minimum_nights", "maximum_minimum_nights",
                "minimum_maximum_nights", "maximum_maximum_nights", "minimum_nights_avg_ntm", "maximum_nights_avg_ntm",
                "calendar_last_scraped", "amenities"
            ],
            "hosts": [
                "host_url", "host_thumbnail_url", "host_picture_url", "host_about"
            ]
        }
        cols_to_drop = [c for c in drop_columns.get(collection_name, []) if c in df.columns]
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)
            self.logger.info(f"Columnas eliminadas de '{collection_name}': {cols_to_drop}")
        return df

    def generate_fact_calendar(self, df_calendar: pd.DataFrame, df_listings: pd.DataFrame) -> pd.DataFrame:
        df_calendar = df_calendar.copy()
        df_calendar["listing_id"] = df_calendar["listing_id"].astype(int)
        df_fact = df_calendar.merge(
            df_listings[["id", "host_id", "accommodates"]],
            left_on="listing_id",
            right_on="id",
            how="left"
        )
        df_fact = df_fact.rename(columns={
            "date": "date_key", "listing_id": "listing_key", "host_id": "host_key"
        })
        return df_fact[["date_key", "listing_key", "host_key", "available", "price", "accommodates"]]

    def generate_fact_reviews(self, df_reviews: pd.DataFrame) -> pd.DataFrame:
        df_reviews = df_reviews.copy()
        df_reviews["date"] = pd.to_datetime(df_reviews["date"], errors="coerce")
        df_reviews = df_reviews.rename(columns={
            "listing_id": "listing_key", "reviewer_id": "guest_key", "date": "date_key"
        })
        return df_reviews[["listing_key", "guest_key", "date_key", "comments"]]

    def generate_dim_date(self, df_dates: pd.Series) -> pd.DataFrame:
        df = pd.DataFrame({"date_key": pd.to_datetime(df_dates.dropna().unique())})
        df = df.sort_values("date_key").reset_index(drop=True)
        df["year"] = df["date_key"].dt.year
        df["month"] = df["date_key"].dt.month
        df["day"] = df["date_key"].dt.day
        df["day_name"] = df["date_key"].dt.day_name()
        df["month_name"] = df["date_key"].dt.month_name()
        df["quarter"] = df["date_key"].dt.quarter
        return df

    def generate_dimensions(self, df_listings, df_hosts, df_reviews, df_calendar, df_guests):
        dim_hosts = df_hosts.copy()
        dim_listings = df_listings[["id", "name", "neighbourhood", "room_type", "accommodates", "price"]].rename(columns={"id": "listing_id"})
        dim_guests = df_guests.rename(columns={"reviewer_id": "guest_id", "reviewer_name": "guest_name"})
        all_dates = pd.concat([df_reviews["date"], df_calendar["date"]], ignore_index=True)
        dim_date = self.generate_dim_date(all_dates)
        return {"dim_hosts": dim_hosts, "dim_listings": dim_listings, "dim_guests": dim_guests, "dim_date": dim_date}

    def build_star_schema(self, df_listings, df_hosts, df_reviews_result, df_calendar):
        df_reviews = df_reviews_result["reviews"]
        df_guests = df_reviews_result["guests"]
        dims = self.generate_dimensions(df_listings, df_hosts, df_reviews, df_calendar, df_guests)
        fact_calendar = self.generate_fact_calendar(df_calendar, df_listings)
        fact_reviews = self.generate_fact_reviews(df_reviews)
        self.logger.info("Modelo estrella generado correctamente.")
        return {**dims, "fact_calendar": fact_calendar, "fact_reviews": fact_reviews}