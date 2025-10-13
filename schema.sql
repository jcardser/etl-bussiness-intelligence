-- ==========================================================
-- 1️⃣ DIM_HOST
-- ==========================================================
CREATE TABLE dim_host (
    host_id BIGINT PRIMARY KEY,
    host_name TEXT,
    host_since DATE,
    host_location TEXT,
    host_about TEXT,
    host_response_time TEXT,
    host_response_rate TEXT,
    host_acceptance_rate TEXT,
    host_is_superhost BOOLEAN,
    host_picture_url TEXT,
    host_listings_count INT,
    host_total_listings_count INT,
    host_verifications TEXT[],
    host_identity_verified BOOLEAN
);

-- ==========================================================
-- 2️⃣ DIM_LISTING
-- ==========================================================
CREATE TABLE dim_listing (
    listing_id BIGINT PRIMARY KEY,
    host_id BIGINT,
    listing_url TEXT,
    name TEXT,
    description TEXT,
    neighbourhood TEXT,
    neighbourhood_cleansed TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    property_type TEXT,
    room_type TEXT,
    accommodates INT,
    bathrooms REAL,
    bedrooms REAL,
    beds REAL,
    amenities TEXT[],
    price NUMERIC(12,2),
    minimum_nights INT,
    maximum_nights INT,
    instant_bookable BOOLEAN,
    review_scores_rating REAL,
    review_scores_accuracy REAL,
    review_scores_cleanliness REAL,
    review_scores_checkin REAL,
    review_scores_communication REAL,
    review_scores_location REAL,
    review_scores_value REAL,
    reviews_per_month REAL,
    estimated_revenue_l365d NUMERIC(12,2)
);

-- ==========================================================
-- 3️⃣ DIM_GUEST
-- ==========================================================
CREATE TABLE dim_guest (
    reviewer_id BIGINT PRIMARY KEY,
    reviewer_name TEXT
);

-- ==========================================================
-- 4️⃣ DIM_DATE
-- ==========================================================
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    full_date DATE UNIQUE,
    year INT,
    month INT,
    day INT,
    day_name TEXT,
    month_name TEXT,
    quarter INT
);

-- ==========================================================
-- 5️⃣ FACT_RESEÑAS
-- ==========================================================
CREATE TABLE fact_reseñas (
    review_id BIGSERIAL PRIMARY KEY,
    listing_id BIGINT,
    date_id INT,
    reviewer_id BIGINT,
    comments TEXT
);

-- ==========================================================
-- 6️⃣ FACT_RESERVAS
-- ==========================================================
CREATE TABLE fact_reservas (
    reserva_id BIGSERIAL PRIMARY KEY,
    listing_id BIGINT,
    date_id INT,
    available BOOLEAN,
    minimum_nights REAL,
    maximum_nights REAL
);

-- ==========================================================
-- 7️⃣ FACT_INGRESOS
-- ==========================================================
CREATE TABLE fact_ingresos (
    ingreso_id BIGSERIAL PRIMARY KEY,
    listing_id BIGINT,
    date_id INT,
    price NUMERIC(12,2),
    adjusted_price NUMERIC(12,2)
);

-- ==========================================================
-- 🔗 RELACIONES ENTRE TABLAS (FOREIGN KEYS)
-- ==========================================================

-- RELACIÓN: host → listings
ALTER TABLE dim_listing
ADD CONSTRAINT fk_listing_host
FOREIGN KEY (host_id)
REFERENCES dim_host(host_id)
ON DELETE SET NULL;

-- FACT_RESEÑAS
ALTER TABLE fact_reseñas
ADD CONSTRAINT fk_reseñas_listing
FOREIGN KEY (listing_id)
REFERENCES dim_listing(listing_id)
ON DELETE CASCADE;

ALTER TABLE fact_reseñas
ADD CONSTRAINT fk_reseñas_date
FOREIGN KEY (date_id)
REFERENCES dim_date(date_id)
ON DELETE CASCADE;

ALTER TABLE fact_reseñas
ADD CONSTRAINT fk_reseñas_guest
FOREIGN KEY (reviewer_id)
REFERENCES dim_guest(reviewer_id)
ON DELETE SET NULL;

-- FACT_RESERVAS
ALTER TABLE fact_reservas
ADD CONSTRAINT fk_reservas_listing
FOREIGN KEY (listing_id)
REFERENCES dim_listing(listing_id)
ON DELETE CASCADE;

ALTER TABLE fact_reservas
ADD CONSTRAINT fk_reservas_date
FOREIGN KEY (date_id)
REFERENCES dim_date(date_id)
ON DELETE CASCADE;

-- FACT_INGRESOS
ALTER TABLE fact_ingresos
ADD CONSTRAINT fk_ingresos_listing
FOREIGN KEY (listing_id)
REFERENCES dim_listing(listing_id)
ON DELETE CASCADE;

ALTER TABLE fact_ingresos
ADD CONSTRAINT fk_ingresos_date
FOREIGN KEY (date_id)
REFERENCES dim_date(date_id)
ON DELETE CASCADE;
