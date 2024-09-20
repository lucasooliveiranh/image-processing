CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    image_name VARCHAR(255),
    image_path VARCHAR(500),  -- Store image file path
    image_data BYTEA          -- Store image binary data
);