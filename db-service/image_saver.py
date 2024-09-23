import psycopg2
import os

def save_image_to_db(image_path):
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('POSTGRES_DB', 'images_db'),
            user=os.environ.get('POSTGRES_USER', 'user'),
            password=os.environ.get('POSTGRES_PASSWORD', 'password'),
            host='db',
            port='5432'
        )
        cursor = conn.cursor()
        
        with open(image_path, 'rb') as file:
            image_data = file.read()

        image_name = os.path.basename(image_path)

        cursor.execute("""
            INSERT INTO images (image_name, image_path, image_data) 
            VALUES (%s, %s, %s)
        """, (image_name, image_path, image_data))

        conn.commit()

        return f"Image {image_name} saved successfully!"
    except Exception as e:
        print(f"Error saving image to DB: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def get_all_images_from_db():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('POSTGRES_DB', 'images_db'),
            user=os.environ.get('POSTGRES_USER', 'user'),
            password=os.environ.get('POSTGRES_PASSWORD', 'password'),
            host='db',
            port='5432'
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM images")
        rows = cursor.fetchall()

        return [row[1] for row in rows]  # Assuming the second column is image_path
    except Exception as e:
        print(f"Error fetching images from DB: {e}")
        raise
    finally:
        cursor.close()
        conn.close()