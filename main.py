from PIL import Image, ImageDraw, ImageFont

def create_custom_palette():
    return {
        1: (0, 0, 0),       # Noir
        2: (255, 0, 0),     # Rouge
        3: (0, 255, 0),     # Vert
        4: (0, 0, 255),     # Bleu
        5: (255, 255, 0),   # Jaune
        6: (255, 165, 0),   # Orange
        7: (255, 20, 147),  # Rose
        8: (255, 255, 255)  # Blanc
    }

def map_colors_to_palette(image, palette):
    width, height = image.size
    image = image.convert('RGB')
    mapped_pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            pixel_color = image.getpixel((x, y))
            closest_color = min(palette.items(), key=lambda c: sum((s - q) ** 2 for s, q in zip(c[1], pixel_color)))[0]
            row.append(closest_color)
        mapped_pixels.append(row)
    return mapped_pixels

def resize_with_aspect_ratio(image, base_pixels, max_pixels):
    w, h = image.size
    if w > h:
        new_w = min(w, max_pixels)
        new_h = int(new_w * h / w)
    else:
        new_h = min(h, max_pixels)
        new_w = int(new_h * w / h)
    return image.resize((new_w, new_h), resample=Image.NEAREST)

def generate_pixel_art(image_path, input_path="", output_path="",  base_pixels=100, max_pixels=100, pixel_size=15):
    
    #On récupère le nom du fichier
    name = image_path.split('.')[0]
    
    #On crée les noms des fichiers de sortie
    output_filename_blank = name + '_blank.png'
    output_filename_colored = name + '_colored.png'


    original_image = Image.open(input_path + image_path)
    resized_image = resize_with_aspect_ratio(original_image, base_pixels, max_pixels)
    palette = create_custom_palette()
    color_indices = map_colors_to_palette(resized_image, palette)

    image_blank = Image.new('RGB', (resized_image.size[0] * pixel_size, resized_image.size[1] * pixel_size), 'white')
    image_colored = Image.new('RGB', (resized_image.size[0] * pixel_size, resized_image.size[1] * pixel_size), 'white')
    draw_blank = ImageDraw.Draw(image_blank)
    draw_colored = ImageDraw.Draw(image_colored)
    font = ImageFont.truetype("arial.ttf", size=int(pixel_size * 0.75)) 

    for y in range(resized_image.size[1]):
        for x in range(resized_image.size[0]):
            color_number = color_indices[y][x]
            color = palette[color_number]
            draw_blank.rectangle([x * pixel_size, y * pixel_size, (x + 1) * pixel_size, (y + 1) * pixel_size], fill="white", outline="black")
            draw_colored.rectangle([x * pixel_size, y * pixel_size, (x + 1) * pixel_size, (y + 1) * pixel_size], fill=color, outline="black")
            text_xy = (x * pixel_size + pixel_size // 2, y * pixel_size + pixel_size // 2)
            draw_blank.text(text_xy, str(color_number), font=font, fill="black", anchor="mm")
            draw_colored.text(text_xy, str(color_number), font=font, fill="black", anchor="mm")

    image_blank.save( output_path + output_filename_blank)
    image_colored.save(output_path + output_filename_colored)



# Utilisation de l'exemple
generate_pixel_art('labrador.png',input_path="image/", output_path="output/")
