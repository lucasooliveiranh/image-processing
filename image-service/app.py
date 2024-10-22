from flask import Flask, request, jsonify
from flask_cors import CORS
from image_generator import (
    generate_high_resolution_image,
    generate_complex_pattern_image,
    generate_generative_art,
    apply_image_filter,
    generate_with_additional_elements,
    batch_process_images,
)
import requests  # Import requests to make HTTP calls
import os

app = Flask(__name__)
CORS(app)  # This will allow CORS for all routes

# Function to save the image path to the db-service
def save_image_to_db(image_path):
    db_service_url = os.environ.get('DB_SERVICE_URL', 'http://db_service:5001/save-image')
    try:
        response = requests.post(db_service_url, json={"image_path": image_path})

        if response.status_code == 200:
            print(f"Image saved to DB: {image_path}")
        else:
            print(f"Failed to save image to DB: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error while trying to save image to DB: {e}")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    text = data.get('text', 'Hello World')
    num_images = data.get('numImages', 1)
    image_type = data.get('type')  # Get the selected type from the request

    image_paths = []

    for i in range(int(num_images)):
        if image_type == 'high_resolution':
            image_path = generate_high_resolution_image(text, i)
        elif image_type == 'complex_patterns':
            image_path = generate_complex_pattern_image(text, i)
        elif image_type == 'generative_art':
            image_path = generate_generative_art(text, i)
        elif image_type == 'image_filters':
            image_path = apply_image_filter(text, i)
        elif image_type == 'additional_elements':
            image_path = generate_with_additional_elements(text, i)
        elif image_type == 'batch_processing':
            image_path = batch_process_images(text, i)
        else:
            image_path = generate_high_resolution_image(text, i)  # Default option

        image_paths.append(image_path)
        save_image_to_db(image_path)  # Save each generated image path to the DB

    return jsonify({"image_paths": image_paths})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
