import os
from PIL import Image

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
img_path = os.path.join(figures_dir, "wechat_state.png")
img = Image.open(img_path)
width, height = img.size
print(f"wechat_state.png: size={width}x{height}")

# Let's inspect rows down the middle column x = width // 2
mid_x = width // 2

# Inspect top 150 pixels for the start node
for y in range(0, 150):
    c = img.getpixel((mid_x, y))
    # Print color transitions
    if y == 0:
        print(f"y={y}: {c}")
        prev_color = c
    elif c != prev_color:
        print(f"y={y}: {prev_color} -> {c}")
        prev_color = c

print("-" * 30)

# Inspect bottom 150 pixels for the end node
for y in range(height - 150, height):
    c = img.getpixel((mid_x, y))
    if y == height - 150:
        print(f"y={y}: {c}")
        prev_color = c
    elif c != prev_color:
        print(f"y={y}: {prev_color} -> {c}")
        prev_color = c
