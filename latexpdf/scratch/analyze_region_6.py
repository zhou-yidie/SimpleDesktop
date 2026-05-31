import os
from PIL import Image

scratch_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\scratch"
img = Image.open(os.path.join(scratch_dir, "region_6.png"))
width, height = img.size

bg_color = (236, 239, 241, 255)

# Print a small summary of colors
colors = {}
for x in range(width):
    for y in range(height):
        p = img.getpixel((x, y))
        diff = sum(abs(p[i] - bg_color[i]) for i in range(3))
        if diff > 30:
            c_rgb = p[:3]
            colors[c_rgb] = colors.get(c_rgb, 0) + 1

# Sort and print top 5 non-bg colors
sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
print("Top 5 text colors:")
for c, count in sorted_colors[:5]:
    print(f"Color {c}: {count} pixels")
