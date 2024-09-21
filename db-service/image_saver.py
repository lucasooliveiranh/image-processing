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

# Function to get all images from the database
def get_all_images_from_db():
    # Example using SQLite, adjust according to your DB setup
    conn = psycopg2.connect(
        dbname="images_db",
        user="user",
        password="password",
        host="db",
        port="5432"
    )
    cursor = conn.cursor()

    # Query to fetch all images (adjust table and columns as needed)
    cursor.execute("SELECT * FROM images")
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Assuming images table has columns (id, image_path), returning image paths
    return [row[1] for row in rows]