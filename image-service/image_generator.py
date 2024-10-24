import os
import uuid
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def generate_high_resolution_image(text, image_number):
    width, height = 3840, 2160  # High resolution
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    draw.text((50, 50), text, fill="black")
    image_path = f"/app/output/high_res_image_{image_number}.png"
    image.save(image_path)
    return image_path

def generate_complex_pattern_image(text, image_number):
    width, height = 1920, 1080
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    for _ in range(1000):
        x0, y0 = random.randint(0, width), random.randint(0, height)
        x1, y1 = random.randint(0, width), random.randint(0, height)
        draw.line([x0, y0, x1, y1], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    image_path = f"/app/output/complex_pattern_image_{image_number}.png"
    image.save(image_path)
    return image_path

def generate_generative_art(text, image_number):
    width, height = 1920, 1080
    noise = np.random.rand(height, width, 3) * 255
    image = Image.fromarray(noise.astype('uint8'))
    image_path = f"/app/output/generative_art_image_{image_number}.png"
    image.save(image_path)
    return image_path

#def apply_image_filter(text, image_number):
#    width, height = 1920, 1080
#    image = Image.new('RGB', (width, height), 'white')
#    draw = ImageDraw.Draw(image)
#    draw.text((50, 50), text, fill="black")
#    image = image.filter(ImageFilter.GaussianBlur(radius=5))
#    image_path = f"/app/output/filtered_image_{image_number}.png"
#    image.save(image_path)
#    return image_path

def generate_with_additional_elements(text, image_number):
    width, height = 1920, 1080
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((50, 50), text, fill="black")
    for _ in range(500):
        x0, y0 = random.randint(0, width), random.randint(0, height)
        x1, y1 = random.randint(0, width), random.randint(0, height)
        draw.rectangle([x0, y0, x1, y1], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    image_path = f"/app/output/complex_image_{image_number}.png"
    image.save(image_path)
    return image_path

#def batch_process_images(text, image_number):
#    image_paths = []
#    for i in range(10):  # Batch generate 10 images
#        image_path = generate_high_resolution_image(text, i)
#        image_paths.append(image_path)
#    return image_paths

def generate_mandelbrot_fractal(text, image_number):
    width, height = 1920, 1080  # Tamanho da imagem
    max_iter = 1000  # Número máximo de iterações
    x_min, x_max = -2.0, 1.0  # Limites do eixo real
    y_min, y_max = -1.5, 1.5  # Limites do eixo imaginário
    
    # Criar a matriz de imagem vazia
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Função para calcular o número de iterações do conjunto de Mandelbrot
    def mandelbrot(c, max_iter):
        z = 0
        n = 0
        while abs(z) <= 2 and n < max_iter:
            z = z*z + c
            n += 1
        return n
    
    # Preencher a imagem com os valores do fractal
    for x in range(width):
        if x % 100 == 0:  # A cada 100 colunas, mostre progresso
            print(f"Processando coluna {x} de {width}...")
        for y in range(height):
            real = x_min + (x / width) * (x_max - x_min)
            imag = y_min + (y / height) * (y_max - y_min)
            c = complex(real, imag)
            m = mandelbrot(c, max_iter)
            
            # Mapear o número de iterações para tons de azul
            color = 255 - int(m * 255 / max_iter)
            image[y, x] = (color, color, 255)  # Azul como cor principal

    # Converter a matriz numpy para uma imagem e salvar
    pil_image = Image.fromarray(image)
    image_path = f"/app/output/mandelbrot_fractal_{image_number}.png"
    pil_image.save(image_path)
    
    return image_path