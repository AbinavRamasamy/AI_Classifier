import os
import string

import random
import numpy as np

from PIL import Image, ImageDraw, ImageFont

IMG_SIZE = 28
CHARS = string.digits + string.ascii_uppercase + string.ascii_lowercase

script_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(script_dir, "Datasets", "DownloadedFonts")
output_folder = os.path.join(script_dir, "Datasets", "GoogleFonts")

os.makedirs(os.path.join(output_folder, "Train"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "Test"), exist_ok=True)

def create_image(char, font_path):
    font = ImageFont.truetype(font_path, size=IMG_SIZE)
    image = Image.new('L', (IMG_SIZE, IMG_SIZE), color=0)
    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox((0, 0), char, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((IMG_SIZE - w) / 2, (IMG_SIZE - h) / 2), char, fill=255, font=font)
    return np.array(image, dtype=np.uint8)

def create_rotated_image(char, font_path):
    font = ImageFont.truetype(font_path, size=IMG_SIZE)
    image = Image.new('L', (IMG_SIZE, IMG_SIZE), color=0)
    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox((0, 0), char, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    angle = random.uniform(-270, 270)

    image = image.rotate(angle, expand=False)

    draw.text(((IMG_SIZE - w) / 2, (IMG_SIZE - h) / 2), char, fill=255, font=font)
    return np.array(image, dtype=np.uint8)

def create_scaled_rotated_image(char, font_path):
    factor = 0.85
    angle = random.uniform(-30, 30)
    font = ImageFont.truetype(font_path, size=int(IMG_SIZE * factor))
    image = Image.new('L', (int(IMG_SIZE * factor), int(IMG_SIZE * factor)), color=0)
    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox((0, 0), char, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((int(IMG_SIZE * factor) - w) / 2, (int(IMG_SIZE * factor) - h) / 2), char, fill=255, font=font)

    image = image.rotate(angle, expand=True)
    image = image.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
    
    return np.array(image, dtype=np.uint8)

def save_ubyte(images, filename):
    if not os.path.exists(filename):
        num_images = len(images)
        rows, cols = IMG_SIZE, IMG_SIZE
        header = np.array([2051, num_images, rows, cols], dtype='>i4').tobytes()
        data = np.array(images).reshape(num_images, rows * cols).astype(np.uint8).tobytes()
        with open(filename, 'wb') as f:
            f.write(header + data)

all_fonts = []
for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.lower().endswith(('.ttf', '.otf')):
            all_fonts.append(os.path.join(root, file))
        else:
            os.remove(os.path.join(root, file))


random.shuffle(all_fonts)
split_index = int(len(all_fonts) * 0.86)

# Process fonts and save to Train/Test folders
for index, font_path in enumerate(all_fonts):
    font_name = os.path.splitext(os.path.basename(font_path))[0]
    if index < split_index:
        out_file = os.path.join(output_folder, "Train", f"{font_name}-images-idx3-ubyte")
    else:
        out_file = os.path.join(output_folder, "Test", f"{font_name}-images-idx3-ubyte")
    
    if os.path.exists(out_file):
        continue

    # Generate images for all characters
    images = []
    for c in CHARS:
        try:
            images.append(create_image(c, font_path))
            images.append(create_rotated_image(c, font_path))
            images.append(create_scaled_rotated_image(c, font_path))
        except OSError as e:
            print(f"Skipping character '{c}' for font {font_path}: {e}")

    # Save images in ubyte format to file
    save_ubyte(images, out_file)
    print(f"[{index}/{len(all_fonts)}]: Saved {len(images)} images for font {font_name} at {out_file}")
