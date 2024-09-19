import psycopg2
import os

def save_image_to_db(image_path):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="images_db",
            user="user",
            password="password",
            host="db",
            port="5432"
        )
        cursor = conn.cursor()

        # Read the image file
        with open(image_path, 'rb') as file:
            binary_data = file.read()

        # Save image to the database
        cursor.execute(
            "INSERT INTO images (image_data) VALUES (%s)", 
            (psycopg2.Binary(binary_data),)
        )

        conn.commit()
        cursor.close()
        conn.close()
        return "Image saved to database successfully."

    except Exception as e:
        return str(e)
