import os
from PIL import Image

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
img_path = os.path.join(figures_dir, "wifi_daemon.png")
img = Image.open(img_path)
width, height = img.size
print(f"wifi_daemon.png: size={width}x{height}")

# Let's count non-white pixels in each column to see where the two columns of the flowchart are.
# Background is pure white (255, 255, 255, 255) or close to it.
col_pixels = []
for x in range(width):
    cnt = 0
    for y in range(height):
        p = img.getpixel((x, y))
        # If not white/transparent
        if sum(p[:3]) < 750 and p[3] > 50:
            cnt += 1
    col_pixels.append(cnt)

# Print columns with non-white pixels
active_cols = []
in_active = False
start = 0
for x in range(width):
    if col_pixels[x] > 0 and not in_active:
        start = x
        in_active = True
    elif col_pixels[x] == 0 and in_active:
        active_cols.append((start, x - 1))
        in_active = False
if in_active:
    active_cols.append((start, width - 1))

print("Active columns:", active_cols)
