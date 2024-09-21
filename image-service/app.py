# image-service/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from image_generator import generate_image
import pika

app = Flask(__name__)
CORS(app)  # This will allow CORS for all routes

# RabbitMQ publish function
def publish_message(image_path):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Declare the queue where the message will be sent
    channel.queue_declare(queue='image_queue')

    # Publish the image path to the queue
    channel.basic_publish(exchange='',
                          routing_key='image_queue',
                          body=image_path)

    # Close the connection
    connection.close()
    
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    text = data.get('text', 'Hello World123')
    num_images = data.get('numImages', 1)  # Get the number of images from the request
    image_paths = []

    for i in range(int(num_images)):
        image_path = generate_image(text, i)  # Pass index to make unique file names
        image_paths.append(image_path)

        # Publish the image path to the queue for the db-service to save
        publish_message(image_path)
        
    return jsonify({"image_paths": image_paths})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)