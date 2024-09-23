from flask import Flask, jsonify, request
from image_saver import save_image_to_db, get_all_images_from_db
import os

app = Flask(__name__)

@app.route('/save-image', methods=['POST'])
def save_image():
    data = request.json
    image_path = data.get('image_path')

    if not image_path or not os.path.exists(image_path):
        return jsonify({"error": "Image not found or path not provided"}), 400

    try:
        result = save_image_to_db(image_path)
        return jsonify({"message": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-images', methods=['GET'])
def get_images():
    try:
        images = get_all_images_from_db()
        return jsonify({"images": images}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)