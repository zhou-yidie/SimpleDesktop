import os
from PIL import Image

scratch_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\scratch"
img = Image.open(os.path.join(scratch_dir, "bottom_box.png"))
width, height = img.size

bg_color = (236, 239, 241, 255)

# Count non-bg pixels in each column
col_non_bg = []
for x in range(width):
    cnt = 0
    for y in range(height):
        p = img.getpixel((x, y))
        diff = sum(abs(p[i] - bg_color[i]) for i in range(3))
        # If it's a border or text
        # Let's ignore the border: the border is at the top (y<=3) and bottom (y>=height-3) and sides
        if y > 5 and y < height - 5 and x > 5 and x < width - 5:
            if diff > 30 and p[3] > 100:
                cnt += 1
    col_non_bg.append(cnt)

# Find discrete word regions separated by at least 15 columns of pure background
word_regions = []
in_word = False
start = 0
consecutive_bg = 0

for x in range(width):
    if col_non_bg[x] > 0:
        if not in_word:
            start = x
            in_word = True
        consecutive_bg = 0
    else:
        if in_word:
            consecutive_bg += 1
            if consecutive_bg >= 15:
                word_regions.append((start, x - 15))
                in_word = False

if in_word:
    word_regions.append((start, width - 1))

print(f"Found {len(word_regions)} word regions:")
for idx, (s, e) in enumerate(word_regions):
    # Print the coordinates and midpoints
    print(f"Region {idx}: x={s} to {e} (width={e-s+1})")
