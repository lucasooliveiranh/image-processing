# image-service/app.py
from flask import Flask, request, jsonify
from image_generator import generate_image

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    text = data.get('text', 'Hello World')
    image_path = generate_image(text)
    
    return jsonify({"image_path": image_path})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)