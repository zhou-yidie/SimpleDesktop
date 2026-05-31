import os
from PIL import Image

scratch_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\scratch"
img = Image.open(os.path.join(scratch_dir, "bottom_box.png"))
width, height = img.size

bg_color = (236, 239, 241, 255)

# We want to find columns that have non-bg pixels
# Let's count non-bg pixels in each column
col_non_bg = []
for x in range(width):
    cnt = 0
    for y in range(height):
        p = img.getpixel((x, y))
        # If color is far from bg_color, treat as text
        diff = sum(abs(p[i] - bg_color[i]) for i in range(3))
        if diff > 30 and p[3] > 100:
            cnt += 1
    col_non_bg.append(cnt)

# Print columns that have text (cnt > 0)
text_regions = []
in_text = False
start = 0
for x in range(width):
    if col_non_bg[x] > 0 and not in_text:
        start = x
        in_text = True
    elif col_non_bg[x] == 0 and in_text:
        text_regions.append((start, x - 1))
        in_text = False
if in_text:
    text_regions.append((start, width - 1))

print("Text regions (columns):", text_regions)
