import os
import random
from PIL import Image, ImageDraw

def generate_dot_image(value, size=(800, 600), dot_size_range=(20, 80)):

    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    max_attempts = 1000
    placed_dots = 0
    attempts = 0
    
    # Adjust dot size based on value
    if value <= 10:
        dot_size = 80
    elif value <= 50:
        dot_size = 60
    else:
        dot_size = 40

    placed_dots_coords = []

    while placed_dots < value and attempts < max_attempts:
        x = random.randint(dot_size, size[0] - dot_size)
        y = random.randint(dot_size, size[1] - dot_size)
        
        # Check for overlap
        overlap = False
        for existing_x, existing_y in placed_dots_coords:
            distance = ((x - existing_x)**2 + (y - existing_y)**2)**0.5
            if distance < dot_size:
                overlap = True
                break
        
        if not overlap:
            draw.ellipse([x-dot_size//2, y-dot_size//2, x+dot_size//2, y+dot_size//2], fill='red')
            placed_dots_coords.append((x, y))
            placed_dots += 1
        
        attempts += 1
    
    if placed_dots < value:
        print(f"Failed to place all dots for value {value}. Placed {placed_dots} out of {value}.")
    
    return img

def main():
    output_dir = 'images/math/dots/'
    os.makedirs(output_dir, exist_ok=True)
    
    for value in range(101):
        img = generate_dot_image(value)
        img.save(os.path.join(output_dir, f'{value}.png'))
        print(f'Generated image for {value} dots')

if __name__ == '__main__':
    main()