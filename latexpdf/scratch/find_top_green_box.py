import os
from PIL import Image

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
img_path = os.path.join(figures_dir, "wifi_daemon.png")
img = Image.open(img_path)
width, height = img.size

# The top green box has a green outline or fill. Let's find green pixels at y <= 150.
# A green pixel will have high G and relatively lower R and B.
green_pixels = []
for x in range(width):
    for y in range(150):
        p = img.getpixel((x, y))
        # Green outline is like (76, 175, 80) or similar (G > 130 and R < 120 and B < 120)
        # Let's check G - R and G - B
        if p[1] > 120 and p[0] < 120 and p[2] < 120:
            green_pixels.append((x, y))

if green_pixels:
    xs = [p[0] for p in green_pixels]
    ys = [p[1] for p in green_pixels]
    print(f"Top green box: x={min(xs)} to {max(xs)}, y={min(ys)} to {max(ys)}")
else:
    print("No green pixels found at the top!")
