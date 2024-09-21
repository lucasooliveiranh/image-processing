from flask import Flask, jsonify
from image_saver import save_image_to_db, get_all_images_from_db
import os
import pika
import threading

app = Flask(__name__)

# Function that will save the image when a message is received from RabbitMQ
def save_image_callback(ch, method, properties, body):
    image_path = body.decode()  # Decode the message received (image path)

    print(f"save_image was called")
    
    if not os.path.exists(image_path):
        print(f"Image not found at path: {image_path}")
    else:
        result = save_image_to_db(image_path)
        print(f"Image saved to DB: {result}")

# RabbitMQ listener to consume messages from the queue
def start_rabbitmq_listener():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Declare the queue to consume messages from
    channel.queue_declare(queue='image_queue')

    # Set up the consumer and link the callback function
    channel.basic_consume(queue='image_queue', on_message_callback=save_image_callback, auto_ack=True)

    print('Waiting for images. To exit press CTRL+C')
    channel.start_consuming()

# Start the RabbitMQ listener in a separate thread so it runs in parallel with the Flask app
rabbitmq_thread = threading.Thread(target=start_rabbitmq_listener)
rabbitmq_thread.start()

# New API endpoint to get all images
@app.route('/get-images', methods=['GET'])
def get_images():
    images = get_all_images_from_db()  # This will fetch all images from the DB
    return jsonify({"images": images})

# Optional: If you still want to keep the manual save route
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