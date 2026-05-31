import os
from PIL import Image, ImageDraw

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
img_path = os.path.join(figures_dir, "wifi_daemon.png")
img = Image.open(img_path)

if img.mode != "RGBA":
    img = img.convert("RGBA")

width, height = img.size
draw = ImageDraw.Draw(img)

# Let's inspect the columns on the left: x = 0 to 20
# If there are any stray lines (non-white pixels), let's cover them with white!
# But wait, does the flowchart have anything on the left that we need to keep?
# The right branch diamond WiFi断连检测? has width and spans from x = 360 to 992 in the original.
# In the cropped image (x shifted by 340):
# Top box is from x = 20 to x = 652.
# So the flowchart elements start very close to the left edge x = 20!
# Let's check what is on the left edge.
# We can cover a small strip on the far left (say, x=0 to 10) with white if there are stray lines.
# Let's do that!
draw.rectangle([0, 0, 10, height], fill=(255, 255, 255, 255))

img.save(img_path)
print("Successfully cleaned left edge of wifi_daemon.png!")
