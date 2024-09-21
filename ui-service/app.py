from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

IMAGE_GENERATION_SERVICE_URL = 'http://image-service:5000/generate'

# Serve the frontend HTML file
@app.route('/')
def index():
    return render_template('index.html')
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)