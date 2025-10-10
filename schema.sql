CREATE TABLE reviews (
    mongo_id VARCHAR(50) PRIMARY KEY,
    listing_id BIGINT,
    review_id BIGINT,
    review_date DATE,
    reviewer_id BIGINT,
    reviewer_name VARCHAR(255),
    comments TEXT
);

CREATE TABLE hosts (
    host_id BIGINT PRIMARY KEY,
    host_url TEXT,
    host_name VARCHAR(255),
    host_since DATE,
    host_location TEXT,
    host_about TEXT,
    host_response_time VARCHAR(50),
    host_response_rate VARCHAR(20),
    host_acceptance_rate VARCHAR(20),
    host_is_superhost BOOLEAN,
    host_thumbnail_url TEXT,
    host_picture_url TEXT,
    host_neighbourhood VARCHAR(255),
    host_listings_count INT,
    host_total_listings_count INT,
    host_verifications TEXT,
    host_has_profile_pic BOOLEAN,
    host_identity_verified BOOLEAN
);

CREATE TABLE listings (
    id BIGINT PRIMARY KEY,
    listing_url TEXT,
    scrape_id BIGINT,
    last_scraped DATE,
    source VARCHAR(100),
    name TEXT,
    description TEXT,
    neighborhood_overview TEXT,
    picture_url TEXT,
    property_type VARCHAR(100),
    room_type VARCHAR(100),
    accommodates INT,
    bathrooms REAL,
    bathrooms_text VARCHAR(50),
    bedrooms INT,
    beds INT,
    price NUMERIC(12,2),
    minimum_nights INT,
    maximum_nights INT,
    minimum_minimum_nights INT,
    maximum_minimum_nights INT,
    minimum_maximum_nights INT,
    maximum_maximum_nights INT,
    minimum_nights_avg_ntm INT,
    maximum_nights_avg_ntm INT,
    has_availability BOOLEAN,
    availability_30 INT,
    availability_60 INT,
    availability_90 INT,
    availability_365 INT,
    availability_eoy INT,
    calendar_last_scraped DATE,
    number_of_reviews INT,
    number_of_reviews_ltm INT,
    number_of_reviews_l30d INT,
    number_of_reviews_ly INT,
    estimated_occupancy_l365d INT,
    estimated_revenue_l365d NUMERIC(14,2),
    first_review DATE,
    last_review DATE,
    review_scores_rating DECIMAL(3,2),
    review_scores_accuracy DECIMAL(3,2),
    review_scores_cleanliness DECIMAL(3,2),
    review_scores_checkin DECIMAL(3,2),
    review_scores_communication DECIMAL(3,2),
    review_scores_location DECIMAL(3,2),
    review_scores_value DECIMAL(3,2),
    reviews_per_month DECIMAL(5,2),
    instant_bookable BOOLEAN,
    calculated_host_listings_count INT,
    calculated_host_listings_count_entire_homes INT,
    calculated_host_listings_count_private_rooms INT,
    calculated_host_listings_count_shared_rooms INT,
    neighbourhood VARCHAR(255),
    neighbourhood_cleansed VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    amenities TEXT,
    host_id BIGINT REFERENCES hosts(host_id)
);

CREATE INDEX idx_listings_host_id ON listings(host_id);
CREATE INDEX idx_listings_neighbourhood ON listings(neighbourhood_cleansed);
CREATE INDEX idx_listings_price ON listings(price);


CREATE TABLE calendar (
    mongo_id VARCHAR(50) PRIMARY KEY,  -- corresponde al _id de MongoDB
    listing_id BIGINT NOT NULL,        -- identificador del alojamiento
    date DATE NOT NULL,                -- fecha de disponibilidad
    available BOOLEAN NOT NULL,        -- si está disponible o no
    price VARCHAR(50),               -- precio convertido de "$50.00"
    minimum_nights INTEGER,
    maximum_nights INTEGER
);
