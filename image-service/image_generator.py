import os
import uuid
from PIL import Image, ImageDraw

def generate_image(text, index):
    output_dir = "/app/output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the directory if it doesn't exist

    img = Image.new('RGB', (200, 100), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((10, 40), text, fill=(255, 255, 0))

    # Save image with a unique file name, using the index to differentiate each image
    image_path = os.path.join(output_dir, f"generated_image_{index}.png")
    img.save(image_path)
    
    return image_path