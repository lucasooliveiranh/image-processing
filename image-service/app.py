# image-service/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from image_generator import generate_high_resolution_image, generate_complex_pattern_image, generate_generative_art, apply_image_filter, generate_with_additional_elements, batch_process_images
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

    return jsonify({"image_paths": image_paths})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)