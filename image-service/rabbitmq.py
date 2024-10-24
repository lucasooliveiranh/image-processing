import pika
import json
import os 
import base64
from image_generator import (
    generate_high_resolution_image,
    generate_complex_pattern_image,
    generate_generative_art,
    #apply_image_filter,
    #generate_with_additional_elements,
    #batch_process_images,
    generate_mandelbrot_fractal
)

# Defina o caminho do diretório de saída para salvar as imagens localmente
OUTPUT_DIR = 'output'

# Verifique se o diretório de saída existe e, se não existir, crie-o
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    
# Função para salvar localmente as imagens geradas
def save_image_locally(image_data, filename):
    image_path = os.path.join(OUTPUT_DIR, filename)
    
    # Se a imagem for uma string base64, converta-a em bytes
    if isinstance(image_data, str):
        image_data = base64.b64decode(image_data)

    # Escreva os dados da imagem como bytes no arquivo
    with open(image_path, 'wb') as f:
        f.write(image_data)
        
    return image_path

def callback(ch, method, properties, body):
    print("Mensagem recebida da fila 'image_queue': %r" % body)

    # Decodifica a mensagem recebida
    try:
        message = json.loads(body)
        text = message.get('text', 'default_text')
        num_images = int(message.get('numImages', 1))
        image_type = message.get('type', 'high_resolution')
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Erro ao processar mensagem: {e}")
        return

    # Processa as imagens com base no tipo recebido
    image_paths = []
    for i in range(num_images):
        filename = f"{image_type}_image_{i}.png"  # Nome do arquivo de saída
        
        # Gera a imagem com base no tipo
        try:
            if image_type == 'high_resolution':
                image_data = generate_high_resolution_image(text, i)
            elif image_type == 'complex_patterns':
                image_data = generate_complex_pattern_image(text, i)
            elif image_type == 'generative_art':
                image_data = generate_generative_art(text, i)
            #elif image_type == 'image_filters':
            #    image_data = apply_image_filter(text, i)
            #elif image_type == 'additional_elements':
            #    image_data = generate_with_additional_elements(text, i)
            #elif image_type == 'batch_processing':
            #    image_data = batch_process_images(text, i)
            elif image_type == 'fractal_mandelbrot':
                image_data = generate_mandelbrot_fractal(text, i)
            else:
                image_data = generate_high_resolution_image(text, i)  # Default option
        except Exception as e:
            print(f"Erro ao gerar a imagem: {e}")
            continue

        # Salva a imagem localmente
        try:
            image_path = save_image_locally(image_data, filename) 
            image_paths.append(image_path)
            print(f"Imagem {filename} salva em {image_path}")
        except Exception as e:
            print(f"Erro ao salvar a imagem: {e}")

def consumir_fila():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='image_queue')

    channel.basic_consume(queue='image_queue', on_message_callback=callback, auto_ack=True)

    print('Esperando mensagens na fila image_queue...')
    channel.start_consuming()
