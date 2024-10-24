from flask import Flask, request, jsonify, Response
from prometheus_client import generate_latest, CollectorRegistry, Gauge, CONTENT_TYPE_LATEST
from flask_cors import CORS
from rabbitmq import (
    consumir_fila
)
import requests  # Import requests to make HTTP calls
import os
import pika
import json
import psutil  # Para obter métricas reais de CPU e memória

app = Flask(__name__)

# Registro de métricas personalizado para evitar conflitos
registry = CollectorRegistry()
cpu_usage = Gauge('cpu_usage', 'CPU Usage (%)', registry=registry)
memory_usage = Gauge('memory_usage', 'Memory Usage (%)', registry=registry)

def collect_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)  # Coleta o uso de CPU
    memory_percent = psutil.virtual_memory().percent  # Coleta o uso de memória

    cpu_usage.set(cpu_percent)  # Define o valor real do uso de CPU
    memory_usage.set(memory_percent)  # Define o valor real do uso de memória

# Endpoint para expor as métricas
@app.route('/metrics')
def metrics():
    collect_metrics()  # Atualiza as métricas antes de retorná-las
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    text = data.get('text', 'Hello World')
    num_images = data.get('numImages', 1)
    image_type = data.get('type')  # Obtenha o tipo de imagem a ser gerado

    # Crie a mensagem que será enviada para a fila
    message = {
        'text': text,
        'numImages': num_images,
        'type': image_type
    }

    # Envie a mensagem para a fila RabbitMQ
    #send_to_queue(message)

    return jsonify({"status": "success", "message": "Data sent to queue"}), 200

if __name__ == '__main__':
    consumir_fila()
    app.run(host='0.0.0.0', port=5000)
