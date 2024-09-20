import psycopg2
import os

def save_image_to_db(image_path):
    
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
        image_data = file.read()

    # Get image name from the path
    image_name = os.path.basename(image_path)

    # Insert image data into the database
    cursor.execute("""
        INSERT INTO images (image_name, image_path, image_data) 
        VALUES (%s, %s, %s)
    """, (image_name, image_path, image_data))

    # Commit the transaction
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

    return f"Image {image_name} saved successfully!"
