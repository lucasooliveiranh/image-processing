from flask import Flask, jsonify
from image_saver import save_image_to_db
import os

app = Flask(__name__)

@app.route('/save-image', methods=['POST'])
def save_image():
    # Example image path in the shared /output directory
    image_path = "/app/output/generated_image.png"

    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    result = save_image_to_db(image_path)
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)