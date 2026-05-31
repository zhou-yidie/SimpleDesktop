import os
from PIL import Image, ImageDraw, ImageFont

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
img_path = os.path.join(figures_dir, "tech_stack.png")
img = Image.open(img_path)

# Ensure it's in RGBA mode
if img.mode != "RGBA":
    img = img.convert("RGBA")

draw = ImageDraw.Draw(img)

# Define the region to cover:
# Region 6 horizontal range is x = 1640 to 2240
# Bottom box vertical range is y = 1843 to 2131
# Background color is (236, 239, 241, 255)
bg_color = (236, 239, 241, 255)
draw.rectangle([1640, 1843, 2240, 2131], fill=bg_color)

# Let's find a suitable font.
font_paths = [
    r"C:\Windows\Fonts\msyh.ttc",  # Microsoft YaHei
    r"C:\Windows\Fonts\msyhbd.ttc", # Microsoft YaHei Bold
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\simsun.ttc"
]

font_path = None
for p in font_paths:
    if os.path.exists(p):
        font_path = p
        break

if not font_path:
    # Fallback to default
    font = ImageFont.load_default()
    print("Warning: standard fonts not found, using default font!")
else:
    # The box height is 288. Let's use font size around 88.
    font = ImageFont.truetype(font_path, 88)

text = "Android 14 (API 34)"
text_color = (44, 62, 80, 255)

# Center the text in the bounding box [1640, 1843, 2240, 2131]
# Bounding box width = 600, height = 288
box_width = 2240 - 1640
box_height = 2131 - 1843

# Get text bounding box to center it
try:
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
except AttributeError:
    # Older Pillow versions
    text_w, text_h = draw.textsize(text, font=font)

# Align to the left/right center. Let's see: in original image, was it centered?
# Yes, it should be centered.
text_x = 1640 + (box_width - text_w) // 2
text_y = 1843 + (box_height - text_h) // 2 - 10 # slight vertical adjustment

draw.text((text_x, text_y), text, fill=text_color, font=font)

# Save the updated image!
img.save(img_path)
print("Successfully fixed tech_stack.png!")
