import os
from PIL import Image, ImageDraw

def generate_image(text):
    output_dir = "/app/output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the directory if it doesn't exist

    img = Image.new('RGB', (200, 100), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((10, 40), text, fill=(255, 255, 0))

    image_path = os.path.join(output_dir, "generated_image.png")
    img.save(image_path)

    return image_path