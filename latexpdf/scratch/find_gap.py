import os
from PIL import Image

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
img_path = os.path.join(figures_dir, "wifi_daemon.png")
img = Image.open(img_path)
width, height = img.size

col_pixels = []
for x in range(width):
    cnt = 0
    for y in range(height):
        p = img.getpixel((x, y))
        if sum(p[:3]) < 750 and p[3] > 50:
            cnt += 1
    col_pixels.append(cnt)

# Print density in 20-pixel blocks to see where the gap is
for x in range(0, width, 40):
    block_sum = sum(col_pixels[x:x+40])
    print(f"Cols {x:3d}-{x+39:3d}: sum={block_sum}")
