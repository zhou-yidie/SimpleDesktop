import os
from PIL import Image

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
img_path = os.path.join(figures_dir, "wechat_state.png")
img = Image.open(img_path)
width, height = img.size

# Let's find the horizontal boundaries of the start box at y = 120
# Background color is (200, 222, 245) or close to it
start_y = 120
row_colors = [img.getpixel((x, start_y)) for x in range(width)]
start_x = -1
end_x = -1
for x, c in enumerate(row_colors):
    # Check if close to (200, 222, 245)
    if abs(c[0] - 200) < 15 and abs(c[1] - 222) < 15 and abs(c[2] - 245) < 15:
        if start_x == -1:
            start_x = x
        end_x = x
print(f"Start box horizontal range at y={start_y}: x={start_x} to {end_x}")

# Let's find the horizontal boundaries of the end box at y = 830
# Background color is (210, 232, 209) or close to it
end_y = 830
row_colors_end = [img.getpixel((x, end_y)) for x in range(width)]
start_x_end = -1
end_x_end = -1
for x, c in enumerate(row_colors_end):
    if abs(c[0] - 210) < 15 and abs(c[1] - 232) < 15 and abs(c[2] - 209) < 15:
        if start_x_end == -1:
            start_x_end = x
        end_x_end = x
print(f"End box horizontal range at y={end_y}: x={start_x_end} to {end_x_end}")
