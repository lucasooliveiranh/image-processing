from flask import Flask, render_template, request, jsonify, Response
from prometheus_client import generate_latest, CollectorRegistry, Gauge, CONTENT_TYPE_LATEST
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

# Função para enviar mensagem à fila RabbitMQ
def send_to_queue(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))  # Conecte-se ao container RabbitMQ
        channel = connection.channel()
        
        # Declara a fila 'image_queue' se ela não existir
        channel.queue_declare(queue='image_queue')

        # Envia a mensagem para a fila em formato JSON
        channel.basic_publish(exchange='', routing_key='image_queue', body=json.dumps(message))
        connection.close()
        print(f"Mensagem enviada para a fila: {message}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para a fila: {e}")

@app.route('/send', methods=['POST'])
def handle_send():
    data = request.json  # Pega os dados enviados pela interface
    
    # Se espera que o campo 'input' tenha text, numImages e type
    user_input = data.get('input')  
    
    # Valida os campos esperados
    if user_input and 'text' in user_input and 'numImages' in user_input and 'type' in user_input:
        send_to_queue(user_input)  # Envia os dados para a fila
        
        return jsonify({'status': 'success', 'message': 'Data sent to queue'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid input data'}), 400

# Serve the frontend HTML file
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Inicia o Flask na porta 5005
    app.run(debug=True, host='0.0.0.0', port=5005)
