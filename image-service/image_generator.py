import os
import uuid
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# def generate_image(text, index):
#    output_dir = "/app/output"
#    if not os.path.exists(output_dir):
#        os.makedirs(output_dir)  # Create the directory if it doesn't exist
#
#    img = Image.new('RGB', (200, 100), color=(73, 109, 137))
#    d = ImageDraw.Draw(img)
#    d.text((10, 40), text, fill=(255, 255, 0))
#
#    # Save image with a unique file name, using the index to differentiate each image
#    image_path = os.path.join(output_dir, f"generated_image_{index}.png")
#    img.save(image_path)
#    
#    return image_path

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

def apply_image_filter(text, image_number):
    width, height = 1920, 1080
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    draw.text((50, 50), text, fill="black")
    image = image.filter(ImageFilter.GaussianBlur(radius=5))
    image_path = f"/app/output/filtered_image_{image_number}.png"
    image.save(image_path)
    return image_path

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

def batch_process_images(text, image_number):
    image_paths = []
    for i in range(10):  # Batch generate 10 images
        image_path = generate_high_resolution_image(text, i)
        image_paths.append(image_path)
    return image_paths
