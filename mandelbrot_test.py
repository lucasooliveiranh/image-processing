from PIL import Image
import numpy as np

def generate_mandelbrot_fractal(image_number):
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
    image_path = f"mandelbrot_fractal_{image_number}.png"
    pil_image.save(image_path)
    
    print(f"Imagem Mandelbrot salva como: {image_path}")
    return image_path

# Testar a função isoladamente
if __name__ == "__main__":
    print("Iniciando a geração do fractal de Mandelbrot...")
    generate_mandelbrot_fractal(1)
    print("Processo finalizado.")