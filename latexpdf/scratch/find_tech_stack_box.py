import os
from PIL import Image

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
img_path = os.path.join(figures_dir, "tech_stack.png")
img = Image.open(img_path)
width, height = img.size

# Let's sample colors down the middle column to find where boxes are.
# Bottom is at y = height - 1. We look at x = width // 2.
mid_x = width // 2
print(f"Image width: {width}, height: {height}")

# Find transition points of colors in the bottom 500 pixels.
prev_color = img.getpixel((mid_x, height - 1))
for y in range(height - 1, height - 600, -1):
    c = img.getpixel((mid_x, y))
    if c != prev_color:
        print(f"Transition at y={y}: {prev_color} -> {c}")
        prev_color = c
