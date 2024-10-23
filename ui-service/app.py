from flask import Flask, render_template, request, jsonify
import pika
import json

app = Flask(__name__)

# Função para enviar mensagem à fila
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
    app.run(debug=True, host='0.0.0.0', port=5005)
