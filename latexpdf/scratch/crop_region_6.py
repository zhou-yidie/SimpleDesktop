import os
from PIL import Image

scratch_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\scratch"
img = Image.open(os.path.join(scratch_dir, "bottom_box.png"))
width, height = img.size

# Region 6: x=1650 to 2230
box = img.crop((1640, 0, 2240, height))
box.save(os.path.join(scratch_dir, "region_6.png"))
print("Saved region_6.png!")
