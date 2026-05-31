import os
from PIL import Image

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
img_path = os.path.join(figures_dir, "wifi_daemon.png")
img = Image.open(img_path)
width, height = img.size

# Let's crop from x=340 to x=1000, y=0 to height
cropped = img.crop((340, 0, 1000, height))
cropped.save(img_path)
print("Successfully cropped and saved wifi_daemon.png!")
